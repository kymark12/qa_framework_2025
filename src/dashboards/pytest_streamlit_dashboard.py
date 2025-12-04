import os
import json
from pathlib import Path

import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ---------- Config ----------
# Remote raw URL served from the `reports` branch (public raw URL)
DEFAULT_REMOTE = "https://raw.githubusercontent.com/kymark12/qa_framework_2025/reports/reports/report.json"
REMOTE_URL = os.environ.get("QA_REMOTE_REPORT_URL", DEFAULT_REMOTE)
LOCAL_REPORT_PATH = Path("reports/report.json")

# Cache TTL (seconds) for how long we keep remote fetch results
CACHE_TTL_SECONDS = 120

# Define the colour scheme globally for consistent use
OUTCOME_COLORS = {
    'passed': '#28a745',  # Green
    'failed': '#dc3545',  # Red
    'skipped': '#ffc107', # Yellow
    'xfailed': '#6c757d', # Gray
    'xpassed': '#17a2b8'  # Teal
}

# ---------- Streamlit UI setup ----------
st.set_page_config(page_title="QA Framework — Test Run Dashboard", layout="wide")
st.title("QA Framework — Test Run Dashboard")

# Sidebar controls
with st.sidebar:
    st.header("Controls")
    if st.button("Force refresh remote report"):
        # Clear cached data and rerun
        st.cache_data.clear()
        st.rerun()
    st.markdown("**Remote report URL:**")
    st.write(REMOTE_URL)

# ---------- Helper: load remote-first with fallback ----------
@st.cache_data(ttl=CACHE_TTL_SECONDS)
def fetch_remote_report(url: str, timeout: int = 8):
    """
    Attempt to fetch JSON from the remote URL.
    Returns parsed JSON dict on success, otherwise raises/returns None.
    Cached for CACHE_TTL_SECONDS seconds.
    """
    try:
        resp = requests.get(url, timeout=timeout)
        if resp.status_code == 200:
            return resp.json()
        else:
            # Non-200 (404 etc) — treat as no remote report
            st.info(f"Remote report returned status {resp.status_code}.")
            return None
    except Exception as e:
        st.info(f"Could not fetch remote report: {e}")
        return None

def load_report_remote_first():
    # Try remote
    remote = fetch_remote_report(REMOTE_URL)
    if remote:
        return remote, "remote"
    # Fallback to local
    if LOCAL_REPORT_PATH.exists():
        try:
            local = json.loads(LOCAL_REPORT_PATH.read_text())
            return local, "local"
        except Exception as e:
            st.error(f"Failed to parse local report.json: {e}")
            return None, None
    return None, None

# ---------- Load report ----------
report, source = load_report_remote_first()
if report is None:
    st.warning("No pytest JSON report found (remote or local). Run tests and ensure CI pushed report.json to the `reports` branch.")
    st.stop()

# Extract metadata
created_at = report.get('created', 'Unknown')
duration = report.get('duration', 0)

if source == "remote":
    st.info(f"📡 Loaded report from remote `reports` branch | Generated: {created_at} | Suite Duration: {duration:.2f}s")
else:
    st.info(f"💾 Loaded report from local file | Generated: {created_at} | Suite Duration: {duration:.2f}s")

# ---------- Build DataFrame ----------
tests = report.get("tests", [])
if not tests:
    st.warning("No tests found in the report.")
    st.stop()

df = pd.json_normalize(tests)

# Debug: Show available columns (optional)
with st.expander("📋 Available columns in report"):
    st.write(list(df.columns))

# Ensure outcome column exists
if 'outcome' in df.columns:
    df['outcome'] = df['outcome'].astype(str)
else:
    st.error("Report missing 'outcome' column")
    st.stop()

# ---------- Summary metrics ----------
st.subheader("Summary")
total = len(df)
passed = (df['outcome'] == 'passed').sum()
failed = (df['outcome'] == 'failed').sum()
skipped = (df['outcome'] == 'skipped').sum()
pass_rate = (passed / total * 100) if total > 0 else 0

# Health indicator
if pass_rate >= 95:
    health_status = "🟢 Excellent"
    health_color = "green"
elif pass_rate >= 80:
    health_status = "🟡 Good"
    health_color = "orange"
else:
    health_status = "🔴 Needs Attention"
    health_color = "red"

st.markdown(f"### Test Suite Health: :{health_color}[{health_status}]")
st.markdown("---")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total", int(total))
col2.metric("Passed", int(passed))
col3.metric("Failed", int(failed))
col4.metric("Skipped", int(skipped))
col5.metric("Pass Rate", f"{pass_rate:.1f}%")

# ---------- CHARTS SECTION ----------
st.header("📊 Test Results Visualization")

# Add test category analysis if markers are available
st.subheader("Test Distribution by Category")
if 'nodeid' in df.columns:
    # Extract test categories from nodeid
    df['test_category'] = df['nodeid'].apply(lambda x: x.split('/')[1] if len(x.split('/')) > 1 else 'other')
    category_counts = df['test_category'].value_counts()
    
    fig_cat, ax_cat = plt.subplots(figsize=(10, 4))
    category_colors = ['#007bff', '#28a745', '#ffc107', '#dc3545']
    bars_cat = ax_cat.bar(category_counts.index, category_counts.values, 
                          color=category_colors[:len(category_counts)], alpha=0.8)
    
    # Add value labels
    for bar in bars_cat:
        height = bar.get_height()
        ax_cat.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=11, weight='bold')
    
    ax_cat.set_xlabel('Test Category', fontsize=12, weight='bold')
    ax_cat.set_ylabel('Count', fontsize=12, weight='bold')
    ax_cat.set_title('Tests by Category (API, UI, Unit)', fontsize=14, weight='bold', pad=20)
    ax_cat.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    st.pyplot(fig_cat)
    plt.close()
    
    st.markdown("---")

# Create two columns for charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Test Outcome Distribution")
    
    # Prepare data for pie chart
    outcome_counts = df['outcome'].value_counts()
    
    # Create pie chart
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    pie_colors = [OUTCOME_COLORS.get(outcome, '#6c757d') for outcome in outcome_counts.index]
    
    wedges, texts, autotexts = ax1.pie(
        outcome_counts.values, 
        labels=outcome_counts.index,
        autopct='%1.1f%%',
        colors=pie_colors,
        startangle=90,
        textprops={'fontsize': 12, 'weight': 'bold'}
    )
    
    # Make percentage text more readable
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(11)
    
    ax1.axis('equal')
    plt.title('Test Outcomes', fontsize=14, weight='bold', pad=20)
    st.pyplot(fig1)
    plt.close()

with chart_col2:
    st.subheader("Test Outcome Bar Chart")
    
    # Create a bar chart
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    
    bar_colors = [OUTCOME_COLORS.get(outcome, '#6c757d') for outcome in outcome_counts.index]
    bars = ax2.bar(outcome_counts.index, outcome_counts.values, color=bar_colors, alpha=0.8)
    
    # ... rest of the code ...
    
    ax2.set_xlabel('Outcome', fontsize=12, weight='bold')
    ax2.set_ylabel('Count', fontsize=12, weight='bold')
    ax2.set_title('Test Results by Outcome', fontsize=14, weight='bold', pad=20)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    st.pyplot(fig2)
    plt.close()

# ---------- Duration Visualization ----------
st.subheader("⏱️ Test Duration Analysis")

# Check for duration column
duration_col = None
for col_name in ['duration', 'call.duration', 'setup.duration']:
    if col_name in df.columns:
        duration_col = col_name
        break

if duration_col:
    # Filter out tests with 0 or very small durations for better visualisation
    df_with_duration = df[df[duration_col] > 0].copy()
    
    if len(df_with_duration) > 0:
        # Sort by duration and take the top 10 for better readability
        top_duration_df = df_with_duration.nlargest(10, duration_col)
        
        fig3, ax3 = plt.subplots(figsize=(12, 6))  # Wider, shorter for better display
        
        # Create a horizontal bar chart
        y_pos = range(len(top_duration_df))
        durations = top_duration_df[duration_col].values
        
        # Colour bars by outcome
        bar_colors_duration = [OUTCOME_COLORS.get(outcome, '#6c757d') 
                              for outcome in top_duration_df['outcome']]
        
        bars = ax3.barh(y_pos, durations, color=bar_colors_duration, alpha=0.8, height=0.6)
        
        # Shorten test names for display - improved
        test_names = []
        for name in top_duration_df['nodeid']:
            parts = name.split('::')
            if len(parts) >= 2:
                short_name = f"{parts[1][:40]}..."  # Show file::test format
            else:
                short_name = parts[-1][:40]
            test_names.append(short_name)
        
        ax3.set_yticks(y_pos)
        ax3.set_yticklabels(test_names, fontsize=9)
        ax3.invert_yaxis()  # Highest duration at top
        ax3.set_xlabel('Duration (seconds)', fontsize=12, weight='bold')
        ax3.set_title('Top 10 Slowest Tests', fontsize=14, weight='bold', pad=20)
        ax3.grid(axis='x', alpha=0.3, linestyle='--')
        
        # Add duration values on bars
        for i, (bar, duration) in enumerate(zip(bars, durations)):
            ax3.text(duration + (max(durations) * 0.01), i, f'{duration:.2f}s',
                    va='center', fontsize=9, weight='bold')
        
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close()

# ---------- Failing tests table ----------
st.subheader("❌ Failing Tests")
if failed > 0:
    st.warning(f"⚠️ {int(failed)} test(s) are currently failing. Expand details below:")
    
    # Build columns list based on what's available
    fail_columns = ['nodeid', 'outcome']
    if 'duration' in df.columns:
        fail_columns.append('duration')
    
    failing_df = df[df['outcome'] == 'failed'][fail_columns].reset_index(drop=True)
    
    # Show the summary table
    st.dataframe(failing_df, use_container_width=True)
    
    # Show detailed error messages in expandable sections
    st.markdown("#### 📝 Error Details")
    for idx, row in df[df['outcome'] == 'failed'].iterrows():
        test_name = row['nodeid'].split('::')[-1]
        with st.expander(f"🔍 {test_name}"):
            st.code(row.get('longrepr', row.get('call.longrepr', 'No error details available')), language='python')
else:
    st.success("✅ No failures - All tests passed!")

# ---------- Slowest tests ----------
st.subheader("🐌 Slowest Tests")

if duration_col:
    display_columns = ['nodeid', duration_col]
    sorted_df = df.sort_values(duration_col, ascending=False).head(10)[display_columns]
    # Standardize column name to 'duration' for display
    if duration_col != 'duration':
        sorted_df = sorted_df.rename(columns={duration_col: 'duration'})
    st.dataframe(sorted_df.reset_index(drop=True), use_container_width=True)
else:
    st.warning("Duration information not available in the report. Available columns: " + ", ".join(df.columns))

# ---------- Footer ----------
st.markdown("---")
st.markdown("**💡 Tip:** Use the 'Force refresh' button in the sidebar to reload the latest test results.")
