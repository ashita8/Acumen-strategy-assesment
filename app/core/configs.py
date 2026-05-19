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

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()