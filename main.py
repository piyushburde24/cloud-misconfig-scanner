from database.database import Base, engine
from scanner.manager import ScannerManager


def create_database():
    Base.metadata.create_all(bind=engine)


def main():

    print("=" * 60)
    print("Cloud Misconfiguration Scanner")
    print("=" * 60)

    create_database()

    manager = ScannerManager()

    findings = manager.run()

    print("\n" + "=" * 60)
    print("SCAN COMPLETE")
    print("=" * 60)

    if not findings:
        print("No findings detected.")
        return

    for index, finding in enumerate(findings, start=1):

        print(f"\nFinding #{index}")

        for key, value in finding.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
