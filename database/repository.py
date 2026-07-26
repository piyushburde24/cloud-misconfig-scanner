"""
Database Repository

Responsible for saving scan results.
"""

from sqlalchemy.orm import Session

from database.models import ScanRun, Finding


class Repository:

    def __init__(self, db: Session):
        self.db = db

    def create_scan(self):
        scan = ScanRun(status="Completed")

        self.db.add(scan)
        self.db.commit()
        self.db.refresh(scan)

        return scan

    def save_findings(self, scan_id, findings):
        """
        Save scanner findings and return the database records.
        """

        records = []

        for finding in findings:

            record = Finding(
                scan_id=scan_id,
                service=finding["service"],
                resource=finding["resource"],
                severity=finding["severity"],
                title=finding["title"],
                description=finding["description"],
                recommendation=finding["recommendation"],
            )

            self.db.add(record)
            records.append(record)

        self.db.commit()

        for record in records:
            self.db.refresh(record)

        return records

    def update_ai_analysis(self, finding_id: int, ai_result: dict):
        """
        Update a finding with Gemini AI analysis.
        """

        finding = self.db.get(Finding, finding_id)

        if not finding:
            return

        finding.ai_explanation = ai_result.get("explanation")
        finding.business_impact = ai_result.get("business_impact")
        finding.console_remediation = ai_result.get("console_remediation")
        finding.cli_remediation = ai_result.get("cli_remediation")

        self.db.commit()

    def get_scan(self, scan_id: int):
        """
        Retrieve a scan by its ID.
        """
        return self.db.get(ScanRun, scan_id)

    def get_findings(self, scan_id: int):
        """
        Retrieve all findings for a scan.
        """
        return (
            self.db.query(Finding)
            .filter(Finding.scan_id == scan_id)
            .all()
        )
