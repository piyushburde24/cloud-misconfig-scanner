from database.database import Base, SessionLocal, engine
from database.repository import Repository

from scanner.manager import ScannerManager
from ai.gemini_client import GeminiClient

from config.logging_config import logger


def create_database():
    """
    Create database tables if they do not exist.
    """
    Base.metadata.create_all(bind=engine)


def main():

    logger.info("=" * 60)
    logger.info("Cloud Misconfiguration Scanner Started")
    logger.info("=" * 60)

    create_database()

    db = SessionLocal()

    try:

        # -----------------------------------
        # Initialize Repository
        # -----------------------------------
        repo = Repository(db)

        # -----------------------------------
        # Run AWS Scan
        # -----------------------------------
        logger.info("Starting AWS security scan...")

        manager = ScannerManager()
        findings = manager.run()

        logger.info(f"Scan completed. {len(findings)} findings discovered.")

        # -----------------------------------
        # Save Scan Metadata
        # -----------------------------------
        scan = repo.create_scan()

        records = repo.save_findings(scan.id, findings)

        logger.info(f"{len(records)} findings saved to SQLite database.")

        if not records:
            logger.info("No findings detected. Skipping Gemini AI analysis.")
            return

        # -----------------------------------
        # Build Gemini Input
        # -----------------------------------
        logger.info("Preparing findings for Gemini AI...")

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

        # -----------------------------------
        # Gemini Analysis
        # -----------------------------------
        logger.info("Sending findings to Gemini AI...")

        client = GeminiClient()

        ai_results = client.analyze_findings(ai_input)

        logger.info("Gemini AI analysis completed successfully.")

        # -----------------------------------
        # Update Database
        # -----------------------------------
        logger.info("Saving AI analysis into database...")

        for result in ai_results:

            repo.update_ai_analysis(
                result["id"],
                result
            )

        logger.info("Database updated successfully.")

        logger.info("=" * 60)
        logger.info("Cloud Scan Finished Successfully")
        logger.info("=" * 60)

    except Exception as e:

        logger.exception(f"Application failed: {e}")

    finally:

        db.close()
        logger.info("Database connection closed.")


if __name__ == "__main__":
    main()
