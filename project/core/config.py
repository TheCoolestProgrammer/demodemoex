from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost/main"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
