from app.ingestion.chunker import chunk_text


def test_chunk_text():
    text = "A" * 2500

    chunks = chunk_text(
        text,
        chunk_size=1000,
        overlap=200,
    )

    assert len(chunks) > 1
    assert all(len(chunk) <= 1000 for chunk in chunks)