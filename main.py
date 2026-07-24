from database.database import Base, SessionLocal, engine
from database.repository import Repository

from scanner.manager import ScannerManager


def create_database():
    Base.metadata.create_all(bind=engine)


def main():

    create_database()

    manager = ScannerManager()

    findings = manager.run()

    db = SessionLocal()

    repo = Repository(db)

    scan = repo.create_scan()

    repo.save_findings(scan.id, findings)

    print(f"\nSaved {len(findings)} findings to SQLite.")

    db.close()


if __name__ == "__main__":
    main()
