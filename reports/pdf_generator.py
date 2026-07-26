"""
PDF Generator
"""

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


class PDFGenerator:

    def generate(self, report, filename):

        styles = getSampleStyleSheet()

        doc = SimpleDocTemplate(filename)

        story = []

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        story.append(
            Paragraph(
                "Cloud Misconfiguration Security Report",
                styles["Title"],
            )
        )

        story.append(Spacer(1, 20))

        # -------------------------------------------------
        # Executive Summary
        # -------------------------------------------------

        story.append(
            Paragraph(
                "<b>Executive Summary</b>",
                styles["Heading1"],
            )
        )

        story.append(
            Paragraph(
                f"Overall Security Score: <b>{report['risk']['score']}/100</b>",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"Total Findings: <b>{len(report['findings'])}</b>",
                styles["Normal"],
            )
        )

        story.append(Spacer(1, 15))

        # -------------------------------------------------
        # Severity Summary Table
        # -------------------------------------------------

        story.append(
            Paragraph(
                "<b>Severity Summary</b>",
                styles["Heading2"],
            )
        )

        severity_data = [
            ["Severity", "Count"]
        ]

        for severity in ["Critical", "High", "Medium", "Low"]:

            severity_data.append([
                severity,
                report["severity_summary"].get(severity, 0),
            ])

        severity_table = Table(severity_data)

        severity_table.setStyle(

            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("GRID", (0, 0), (-1, -1), 1, colors.black),

                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ])
        )

        story.append(severity_table)

        story.append(Spacer(1, 20))

        # -------------------------------------------------
        # Findings Table
        # -------------------------------------------------

        story.append(
            Paragraph(
                "<b>Detailed Findings</b>",
                styles["Heading1"],
            )
        )

        findings_table = [
            [
                "Service",
                "Severity",
                "Resource",
                "Title",
            ]
        ]

        for finding in report["findings"]:

            findings_table.append([
                finding.service,
                finding.severity,
                finding.resource,
                finding.title,
            ])

        table = Table(findings_table)

        table.setStyle(

            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("GRID", (0, 0), (-1, -1), 1, colors.black),

                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ])
        )

        story.append(table)

        story.append(Spacer(1, 20))

        # -------------------------------------------------
        # AI Recommendations
        # -------------------------------------------------

        story.append(
            Paragraph(
                "<b>Gemini AI Recommendations</b>",
                styles["Heading1"],
            )
        )

        for finding in report["findings"]:

            story.append(
                Paragraph(
                    f"<b>{finding.title}</b>",
                    styles["Heading2"],
                )
            )

            story.append(
                Paragraph(
                    f"<b>Resource:</b> {finding.resource}",
                    styles["Normal"],
                )
            )

            story.append(
                Paragraph(
                    f"<b>Explanation:</b> {finding.ai_explanation or 'N/A'}",
                    styles["Normal"],
                )
            )

            story.append(
                Paragraph(
                    f"<b>Business Impact:</b> {finding.business_impact or 'N/A'}",
                    styles["Normal"],
                )
            )

            story.append(
                Paragraph(
                    f"<b>AWS Console:</b> {finding.console_remediation or 'N/A'}",
                    styles["Normal"],
                )
            )

            story.append(
                Paragraph(
                    f"<b>AWS CLI:</b> {finding.cli_remediation or 'N/A'}",
                    styles["Normal"],
                )
            )

            story.append(Spacer(1, 15))

        doc.build(story)
