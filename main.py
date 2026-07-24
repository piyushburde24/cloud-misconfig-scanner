from database.database import Base, engine
from scanner.s3_scanner import S3Scanner


def create_database():
    Base.metadata.create_all(bind=engine)


def main():

    print("=" * 60)
    print("Cloud Misconfiguration Scanner")
    print("=" * 60)

    create_database()

    scanner = S3Scanner()

    findings = scanner.scan()

    print("\nFindings\n")

    if not findings:

        print("No issues found.")

    else:

        for finding in findings:

            print("-" * 50)

            for key, value in finding.items():
                print(f"{key}: {value}")


if __name__ == "__main__":
    main()
