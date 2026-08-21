from app.ingestion.chunker import chunk_pages


def test_chunk_pages_preserves_page_number():

    pages = [
        {
            "page_number": 1,
            "text": "A" * 100,
        },
        {
            "page_number": 2,
            "text": "B" * 100,
        },
    ]

    chunks = chunk_pages(
        pages,
        chunk_size=50,
        overlap=10,
    )

    assert len(chunks) > 0

    assert chunks[0]["page_number"] == 1
    assert chunks[0]["chunk_index"] == 0

    assert any(
        chunk["page_number"] == 2
        for chunk in chunks
    )