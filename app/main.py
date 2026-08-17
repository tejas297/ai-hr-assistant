from fastapi import FastAPI

app= FastAPI(
    title="AI HR Assistant",
    description="AI-powered HR policy assistant",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return{
    "status": "ok",
    "service": "AI HR Assistant",
    }