from langchain_groq import ChatGroq
from langchain_openrouter import ChatOpenRouter
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

from ai.config.config import (
    GROQ_API_KEY,
    MODEL_NAME,
    OPENROUTER_API_KEY
)

def get_llm():

    llm2 = ChatGroq(
        model=MODEL_NAME,
        temperature=0
    )

    llm = ChatOpenRouter(
        model=MODEL_NAME,
        temperature=0
    )

    # llm3 = ChatOpenAI(
    #     model = "gpt-4o-mini",
    #     temperature = 0.5
    # )


    return llm