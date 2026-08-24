from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class SourceResponse(BaseModel):
    document_name: str
    page_number: int


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]