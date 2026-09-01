from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(
        min_length=1,
        max_length=100,
    )

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
    reasoning: str = ""


class UploadResponse(BaseModel):
    success: bool
    message: str
    document_name: str
    chunks_created: int


class UploadError(BaseModel):
    filename: str
    error: str


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=200)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    message: str = "Login successful"