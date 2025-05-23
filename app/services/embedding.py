import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(text: str) -> list:
    """
    Convert text into an embedding vector using OpenAI's embedding model.
    """
    try:
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response["data"][0]["embedding"]
    except Exception as e:
        print(f"❌ Embedding failed: {e}")
        return []
