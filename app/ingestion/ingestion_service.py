from sqlalchemy.orm import Session

from app.ingestion.pdf_loader import extract_text_from_pdf
from app.ingestion.chunker import chunk_pages
from app.ingestion.embedding import generate_embedding
from app.database.models import DocumentChunk


def ingest_pdf(
    db: Session,
    file_path: str,
    document_name: str,
) -> int:
    """
    Extract, chunk, embed, and store a PDF document.

    Returns the number of chunks stored.
    """

    # 1. Extract text from PDF
    pages = extract_text_from_pdf(file_path)

    # 2. Create chunks while preserving page metadata
    chunks = chunk_pages(pages)

    if not chunks:
        raise ValueError(
            f"No text chunks found in document: {document_name}"
        )

    # 3. Generate embeddings and prepare database records
    document_chunks = []

    for chunk in chunks:

        embedding = generate_embedding(
            chunk["content"]
        )

        document_chunk = DocumentChunk(
            document_name=document_name,
            page_number=chunk["page_number"],
            chunk_index=chunk["chunk_index"],
            content=chunk["content"],
            embedding=embedding,
        )

        document_chunks.append(document_chunk)

    # 4. Store everything in PostgreSQL
    db.add_all(document_chunks)

    db.commit()

    return len(document_chunks)