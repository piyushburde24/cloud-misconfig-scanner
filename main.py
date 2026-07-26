from database.database import Base, SessionLocal, engine
from database.repository import Repository

from scanner.manager import ScannerManager
from ai.gemini_client import GeminiClient


def create_database():
    Base.metadata.create_all(bind=engine)


def main():
    create_database()

    db = SessionLocal()
    repo = Repository(db)

    # Step 1: Run AWS Scan
    manager = ScannerManager()
    findings = manager.run()

    # Step 2: Save Scan
    scan = repo.create_scan()

    records = repo.save_findings(scan.id, findings)

    print(f"\nSaved {len(records)} findings to SQLite.")

    if not records:
        print("No findings found. Skipping AI analysis.")
        db.close()
        return

    # Step 3: Build payload for Gemini
    ai_input = []

    for record in records:
        ai_input.append({
            "id": record.id,
            "service": record.service,
            "resource": record.resource,
            "severity": record.severity,
            "title": record.title,
            "description": record.description,
            "recommendation": record.recommendation,
        })

    # Step 4: Analyze with Gemini
    print("\nAnalyzing findings with Gemini AI...\n")

    client = GeminiClient()
    ai_results = client.analyze_findings(ai_input)

    # Step 5: Update database
    for result in ai_results:
        repo.update_ai_analysis(
            result["id"],
            result
        )

    print("AI analysis saved successfully.")

    db.close()


if __name__ == "__main__":
    main()
