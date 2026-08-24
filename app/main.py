from fastapi import FastAPI
from app.api.chat import router as chat_router
app= FastAPI(
    title="AI HR Assistant",
    description="AI-powered HR policy assistant",
    version="0.1.0"
)
app.include_router(chat_router)

@app.get("/health")
def health_check():
    return{
    "status": "ok",
    "service": "AI HR Assistant",
    }