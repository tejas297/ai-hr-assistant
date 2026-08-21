from app.database.connection import SessionLocal
from app.ingestion.ingestion_service import ingest_pdf


PDF_PATH = "documents/asset_approval_policy.pdf"
DOCUMENT_NAME = "asset_approval_policy.pdf"


def main():

    db = SessionLocal()

    try:

        count = ingest_pdf(
            db=db,
            file_path=PDF_PATH,
            document_name=DOCUMENT_NAME,
        )

        print(
            f"Successfully ingested "
            f"{count} chunks from {DOCUMENT_NAME}"
        )

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()