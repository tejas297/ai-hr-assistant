from dataclasses import dataclass

from app.database.models import DocumentChunk


@dataclass
class SearchResult:
    chunk: DocumentChunk
    distance: float