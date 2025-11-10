import os
import json
from pathlib import Path

import requests
import pandas as pd
import streamlit as st

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
        st.experimental_rerun()
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

# ---------- Failing tests table ----------
st.subheader("Failing Tests")
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
    st.dataframe(failing_df)
else:
    st.write("No failures")

# ---------- Slowest tests ----------
st.subheader("Slowest Tests")
# Check for possible duration columns (including nested)
duration_col = None
for col_name in ['duration', 'call.duration', 'setup.duration']:
    if col_name in df.columns:
        duration_col = col_name
        break

if duration_col:
    display_columns = ['nodeid', duration_col]
    sorted_df = df.sort_values(duration_col, ascending=False).head(10)[display_columns]
    # Standardize column name to 'duration' for display
    if duration_col != 'duration':
        sorted_df = sorted_df.rename(columns={duration_col: 'duration'})
    st.dataframe(sorted_df.reset_index(drop=True))
else:
    st.warning("Duration information not available in the report. Available columns: " + ", ".join(df.columns))

# ---------- (Optional) extra sections you may add later ----------
# - Trend charts (requires history db or archived JSONs)
# - Flaky detection (requires historical runs)
# - Links to Allure artifacts or screenshots
