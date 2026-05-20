from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):

    APP_NAME: str = "wealth-advisor-ai"

    ENVIRONMENT: str = "development"

    LOG_LEVEL: str = "INFO"

    DATABASE_URL: str = (
        "postgresql://postgres:postgres@localhost:5433/wealth_advisor"
    )

    POSTGRES_USER: str

    POSTGRES_PASSWORD: str

    POSTGRES_HOST: str

    POSTGRES_PORT: int

    POSTGRES_DB: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    GROQ_API_KEY: str

    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    GROQ_TEMPERATURE: float = 0.2

    GROQ_MAX_RETRIES: int = 3


settings = Settings()