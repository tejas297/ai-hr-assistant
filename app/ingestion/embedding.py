import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not configured")


client = OpenAI(api_key=OPENAI_API_KEY)


EMBEDDING_MODEL = "text-embedding-3-small"


def generate_embedding(text: str) -> list[float]:
    """
    Generate an embedding vector for a single text chunk.
    """

    if not text.strip():
        raise ValueError("Cannot generate embedding for empty text")

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )

    return response.data[0].embedding