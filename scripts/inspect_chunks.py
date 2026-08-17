from app.ingestion.pdf_loader import extract_text_from_pdf
from app.ingestion.chunker import chunk_text


PDF_PATH = "documents/asset_approval_policy.pdf"


pages = extract_text_from_pdf(PDF_PATH)

chunk_index = 0

for page in pages:

    chunks = chunk_text(page["text"])

    for chunk in chunks:

        print("=" * 80)
        print(f"PAGE: {page['page_number']}")
        print(f"CHUNK: {chunk_index}")
        print("=" * 80)
        print(chunk)

        chunk_index += 1