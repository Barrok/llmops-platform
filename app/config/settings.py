from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "LLMOps Platform"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333

    model_config = SettingsConfigDict(
        env_file=".env",
    )


settings = Settings()
