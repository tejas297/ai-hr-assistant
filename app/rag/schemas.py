from dataclasses import dataclass


@dataclass
class Source:
    document_name: str
    page_number: int


@dataclass
class RAGResponse:
    answer: str
    sources: list[Source]
    reasoning: str = ""