from app.ingestion.pdf_loader import extract_text_from_pdf


PDF_PATH = "documents/asset_approval_policy.pdf"


pages = extract_text_from_pdf(PDF_PATH)

for page in pages:
    print("=" * 80)
    print(f"PAGE {page['page_number']}")
    print("=" * 80)
    print(page["text"])