from database.database import SessionLocal
from database.models import ScanRun

from database.repository import Repository

from reports.report_builder import ReportBuilder
from reports.pdf_generator import PDFGenerator

from security.risk_score import RiskScoreCalculator


def main():

    db = SessionLocal()

    try:

        repo = Repository(db)

        # Get the latest scan
        latest_scan = (
            db.query(ScanRun)
            .order_by(ScanRun.id.desc())
            .first()
        )

        if latest_scan is None:
            print("No scans found in the database.")
            return

        findings = repo.get_findings(latest_scan.id)

        risk = RiskScoreCalculator.calculate(findings)

        report = ReportBuilder.build(
            latest_scan,
            findings,
            risk
        )

        PDFGenerator().generate(
            report,
            "security_report.pdf"
        )

        print(f"PDF generated successfully for Scan ID {latest_scan.id}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
