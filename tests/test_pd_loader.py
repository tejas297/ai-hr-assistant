from app.ingestion.pdf_loader import extract_text_from_pdf


def test_extract_pdf():
    pages = extract_text_from_pdf("documents/asset_approval_policy.pdf")

    assert len(pages) > 0

    for page in pages:
        assert "page_number" in page
        assert "text" in page