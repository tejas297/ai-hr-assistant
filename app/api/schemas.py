from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=1000,
    )


class SourceResponse(BaseModel):
    document_name: str
    page_number: int


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]