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

if source == "remote":
    st.info("Loaded report from remote `reports` branch.")
else:
    st.info("Loaded report from local file: reports/report.json")

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

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total", int(total))
col2.metric("Passed", int(passed))
col3.metric("Failed", int(failed))
col4.metric("Skipped", int(skipped))

# ---------- CHARTS SECTION ----------
st.header("📊 Test Results Visualization")

# Create two columns for charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Test Outcome Distribution")
    
    # Prepare data for pie chart
    outcome_counts = df['outcome'].value_counts()
    
    # Create pie chart
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    colors = {
        'passed': '#28a745',  # Green
        'failed': '#dc3545',  # Red
        'skipped': '#ffc107'  # Yellow
    }
    pie_colors = [colors.get(outcome, '#6c757d') for outcome in outcome_counts.index]
    
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
    
    # Create bar chart
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    
    bar_colors = [colors.get(outcome, '#6c757d') for outcome in outcome_counts.index]
    bars = ax2.bar(outcome_counts.index, outcome_counts.values, color=bar_colors, alpha=0.8)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=12, weight='bold')
    
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
    # Filter out tests with 0 or very small durations for better visualization
    df_with_duration = df[df[duration_col] > 0].copy()
    
    if len(df_with_duration) > 0:
        # Sort by duration and take top 15 for readability
        top_duration_df = df_with_duration.nlargest(15, duration_col)
        
        fig3, ax3 = plt.subplots(figsize=(10, 8))
        
        # Create horizontal bar chart
        y_pos = range(len(top_duration_df))
        durations = top_duration_df[duration_col].values
        
        # Color bars by outcome
        bar_colors_duration = [colors.get(outcome, '#6c757d') 
                              for outcome in top_duration_df['outcome']]
        
        bars = ax3.barh(y_pos, durations, color=bar_colors_duration, alpha=0.7)
        
        # Shorten test names for display
        test_names = [name.split('::')[-1][:50] for name in top_duration_df['nodeid']]
        ax3.set_yticks(y_pos)
        ax3.set_yticklabels(test_names, fontsize=9)
        ax3.invert_yaxis()  # Highest duration at top
        ax3.set_xlabel('Duration (seconds)', fontsize=12, weight='bold')
        ax3.set_title('Top 15 Slowest Tests', fontsize=14, weight='bold', pad=20)
        ax3.grid(axis='x', alpha=0.3, linestyle='--')
        
        # Add duration values on bars
        for i, (bar, duration) in enumerate(zip(bars, durations)):
            ax3.text(duration, i, f' {duration:.2f}s',
                    va='center', fontsize=9, weight='bold')
        
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close()
        
        # Show statistics
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        with col_stat1:
            st.metric("Avg Duration", f"{df_with_duration[duration_col].mean():.2f}s")
        with col_stat2:
            st.metric("Max Duration", f"{df_with_duration[duration_col].max():.2f}s")
        with col_stat3:
            st.metric("Total Time", f"{df_with_duration[duration_col].sum():.2f}s")
    else:
        st.info("No duration data available for visualization")
else:
    st.warning("Duration information not available in the report.")

# ---------- Failing tests table ----------
st.subheader("❌ Failing Tests")
if failed > 0:
    # Build columns list based on what's available
    fail_columns = ['nodeid']
    if 'duration' in df.columns:
        fail_columns.append('duration')
    # prefer 'longrepr' or nested 'call.longrepr'
    if 'longrepr' in df.columns:
        fail_columns.append('longrepr')
    elif 'call.longrepr' in df.columns:
        fail_columns.append('call.longrepr')

    # Some normalization for nested names display
    failing_df = df[df['outcome'] == 'failed'][fail_columns].reset_index(drop=True)
    # If 'call.longrepr' exists, rename to 'longrepr' for display
    if 'call.longrepr' in failing_df.columns:
        failing_df = failing_df.rename(columns={'call.longrepr': 'longrepr'})
    st.dataframe(failing_df, use_container_width=True)
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
