from langchain_groq import ChatGroq

from app.core.configs import settings


class LLMService:

    _instance = None

    @classmethod
    def get_llm(cls):

        if cls._instance is None:

            cls._instance = ChatGroq(
                groq_api_key=settings.GROQ_API_KEY,
                model_name=settings.GROQ_MODEL,
                temperature=settings.GROQ_TEMPERATURE,
            )

        return cls._instance