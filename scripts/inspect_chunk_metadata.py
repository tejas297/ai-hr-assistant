from app.ingestion.pdf_loader import extract_text_from_pdf
from app.ingestion.chunker import chunk_pages


PDF_PATH = "documents/asset_approval_policy.pdf"


pages = extract_text_from_pdf(PDF_PATH)

chunks = chunk_pages(pages)

print("Total pages:", len(pages))
print("Total chunks:", len(chunks))

print("\nFirst 5 chunks:\n")

for chunk in chunks[:5]:

    print("=" * 80)

    print("Page:", chunk["page_number"])
    print("Chunk:", chunk["chunk_index"])
    print("Content:")
    print(chunk["content"][:500])