from langchain_groq import ChatGroq
from app.core.configs import settings


def get_groq_llm(
    temperature: float = 0.2,
    model: str = "llama-3.3-70b-versatile"
):

    return ChatGroq(
        groq_api_key=settings.GROQ_API_KEY,
        model_name=model,
        temperature=temperature,
    )