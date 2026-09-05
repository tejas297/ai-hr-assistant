import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.admin import router as admin_router

load_dotenv()

app = FastAPI(
    title="AI HR Assistant",
    description="AI-powered HR policy assistant",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173","https://d22l0scvhdklsg.cloudfront.net"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(admin_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "AI HR Assistant",
    }