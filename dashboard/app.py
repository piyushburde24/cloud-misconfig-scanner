import sys
from pathlib import Path

# Add project root to Python path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import streamlit as st

from database.database import SessionLocal
from database.models import ScanRun


st.set_page_config(
    page_title="Cloud Misconfiguration Scanner",
    page_icon="☁️",
    layout="wide",
)

st.title("☁️ Cloud Misconfiguration Scanner")
st.subheader("Security Dashboard")

db = SessionLocal()

try:

    latest_scan = (
        db.query(ScanRun)
        .order_by(ScanRun.id.desc())
        .first()
    )

    if latest_scan is None:

        st.warning("No scans found.")

    else:

        st.success(f"Latest Scan ID: {latest_scan.id}")

        st.write(f"**Status:** {latest_scan.status}")
        st.write(f"**Started At:** {latest_scan.started_at}")

finally:

    db.close()
