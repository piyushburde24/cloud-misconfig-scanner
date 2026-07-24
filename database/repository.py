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

        scan = ScanRun(
            status="Completed"
        )

        self.db.add(scan)
        self.db.commit()
        self.db.refresh(scan)

        return scan

    def save_findings(self, scan_id, findings):

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

        self.db.commit()
