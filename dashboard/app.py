import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import streamlit as st
import plotly.express as px

from database.database import SessionLocal
from database.models import ScanRun
from database.repository import Repository
from security.risk_score import RiskScoreCalculator
from reports.charts import ChartBuilder


st.set_page_config(
    page_title="Cloud Misconfiguration Scanner",
    page_icon="☁️",
    layout="wide",
)

st.title("☁️ Cloud Misconfiguration Scanner")
st.subheader("Security Dashboard")

db = SessionLocal()

try:

    repo = Repository(db)

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

        findings = repo.get_findings(latest_scan.id)

        # -------------------------
        # Filters
        # -------------------------

        st.subheader("Filters")

        services = ["All"] + sorted(
            {f.service for f in findings}
        )

        severities = [
            "All",
            "Critical",
            "High",
            "Medium",
            "Low",
        ]

        col1, col2 = st.columns(2)

        selected_service = col1.selectbox(
            "AWS Service",
            services,
        )

        selected_severity = col2.selectbox(
            "Severity",
            severities,
        )

        filtered_findings = findings

        if selected_service != "All":

            filtered_findings = [
                f for f in filtered_findings
                if f.service.strip().lower()
                == selected_service.strip().lower()
            ]

        if selected_severity != "All":

            filtered_findings = [
                f for f in filtered_findings
                if f.severity.strip().lower()
                == selected_severity.strip().lower()
            ]

        # -------------------------
        # Risk Score
        # -------------------------

        risk = RiskScoreCalculator.calculate(filtered_findings)

        m1, m2, m3, m4, m5, m6 = st.columns(6)

        m1.metric("🛡️ Score", risk["score"])
        m2.metric("🔴 Critical", risk["critical"])
        m3.metric("🟠 High", risk["high"])
        m4.metric("🟡 Medium", risk["medium"])
        m5.metric("🟢 Low", risk["low"])
        m6.metric("📋 Findings", len(filtered_findings))

        st.divider()

        # -------------------------
        # Charts
        # -------------------------

        st.subheader("Security Analytics")

        severity_df = ChartBuilder.severity_chart(filtered_findings)
        service_df = ChartBuilder.service_chart(filtered_findings)

        left, right = st.columns(2)

        with left:

            if not severity_df.empty:

                fig = px.pie(
                    severity_df,
                    names="Severity",
                    values="Count",
                    title="Findings by Severity",
                )

                st.plotly_chart(
                    fig,
                    width="stretch",
                )

            else:

                st.info("No severity data available.")

        with right:

            if not service_df.empty:

                fig = px.bar(
                    service_df,
                    x="Service",
                    y="Count",
                    title="Findings by AWS Service",
                )

                st.plotly_chart(
                    fig,
                    width="stretch",
                )

            else:

                st.info("No service data available.")

        st.divider()

        # -------------------------
        # Findings Table
        # -------------------------

        st.subheader("Latest Findings")

        if filtered_findings:

            table = []

            for finding in filtered_findings:

                table.append(
                    {
                        "Service": finding.service,
                        "Resource": finding.resource,
                        "Severity": finding.severity,
                        "Title": finding.title,
                        "Description": finding.description,
                    }
                )

            st.dataframe(
                table,
                width="stretch",
                hide_index=True,
            )

        else:

            st.info("No findings match the selected filters.")

finally:

    db.close()
