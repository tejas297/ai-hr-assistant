# --- AI HR Assistant backend image ---
# Built for CPU-only deployment (App Runner / ECS Fargate have no GPU).
FROM python:3.12-slim

WORKDIR /app

# System deps needed by psycopg2 / pymupdf at build time
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install CPU-only torch first (the requirements file's default torch wheel
# assumes CUDA and is 3-4GB+ larger than needed here)
COPY requirements-docker.txt .
RUN grep -v '^torch==' requirements-docker.txt > requirements-notorch.txt \
    && pip install --no-cache-dir torch==2.13.0 --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements-notorch.txt

COPY app ./app
COPY scripts ./scripts

# Cloud Run/App Runner/ECS all pass PORT or expect a fixed port — 8000 is fine,
# just make sure it matches whatever you set as the service port in AWS.
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
