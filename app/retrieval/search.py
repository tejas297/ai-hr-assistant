from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import DocumentChunk
from app.ingestion.embedding import generate_embedding
from app.retrieval.schemas import SearchResult

def search_similar_chunks(
    db: Session,
    query: str,
    top_k: int = 5,
    distance_threshold: float = 0.5,

) -> list[SearchResult]:
    """
    Find the most semantically similar document chunks
    for a user query.
    """

    if not query.strip():
        raise ValueError("Query cannot be empty")

    query_embedding = generate_embedding(query)

    # Use the cosine distance between the query embedding and the document chunk embeddings
    distance = DocumentChunk.embedding.cosine_distance(
        query_embedding
    )

    statement = (
          select(DocumentChunk, distance.label("distance"))
          .where(distance <= distance_threshold)
        .order_by(distance)
        .limit(top_k)
    )

    rows = db.execute(statement).all()
    return [
        SearchResult(
            chunk=chunk,
            distance=float(distance),
        )
        for chunk, distance in rows
    ]

    # return results