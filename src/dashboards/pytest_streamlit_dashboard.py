import json
from pathlib import Path

import pandas as pd
import streamlit as st

REPORT_PATH = Path("reports/report.json")

st.title("QA Framework — Test Run Dashboard")

if not REPORT_PATH.exists():
    st.warning("No pytest JSON report found at reports/report.json. Run tests first.")
else:
    data = json.loads(REPORT_PATH.read_text())
    # pytest-json-report structure: data['tests'] list with detailed test result objects
    tests = data.get("tests", [])
    
    if not tests:
        st.warning("No tests found in the report.")
    else:
        df = pd.json_normalize(tests)
        
        # Debug: Show available columns (optional, can be removed later)
        with st.expander("📋 Available columns in report"):
            st.write(list(df.columns))
        
        # Ensure outcome column exists
        if 'outcome' in df.columns:
            df['outcome'] = df['outcome'].astype(str)
        else:
            st.error("Report missing 'outcome' column")
            st.stop()
        
        st.subheader("Summary")
        total = len(df)
        passed = (df['outcome'] == 'passed').sum()
        failed = (df['outcome'] == 'failed').sum()
        skipped = (df['outcome'] == 'skipped').sum()
        st.metric("Total", total)
        st.metric("Passed", passed)
        st.metric("Failed", failed)
        st.metric("Skipped", skipped)

        st.subheader("Failing Tests")
        if failed > 0:
            # Build columns list based on what's available
            fail_columns = ['nodeid']
            if 'duration' in df.columns:
                fail_columns.append('duration')
            if 'longrepr' in df.columns:
                fail_columns.append('longrepr')
            elif 'call.longrepr' in df.columns:
                fail_columns.append('call.longrepr')
            
            st.dataframe(df[df['outcome']=='failed'][fail_columns].reset_index(drop=True))
        else:
            st.write("No failures")

        st.subheader("Slowest Tests")
        # Check if duration column exists, try common alternatives
        duration_col = None
        for col_name in ['duration', 'call.duration', 'setup.duration']:
            if col_name in df.columns:
                duration_col = col_name
                break
        
        if duration_col:
            display_columns = ['nodeid', duration_col]
            sorted_df = df.sort_values(duration_col, ascending=False).head(10)[display_columns]
            # Rename column for display if it's nested
            if duration_col != 'duration':
                sorted_df = sorted_df.rename(columns={duration_col: 'duration'})
            st.dataframe(sorted_df)
        else:
            st.warning("Duration information not available in the report. Available columns: " + ", ".join(df.columns))
