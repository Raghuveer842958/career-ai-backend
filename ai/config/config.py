from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

VECTOR_DB_PATH = "ai/vectorstore"