from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    DATABASE_URL: str = 'sqlite:///./dev.db'
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_SUPERUSER_EMAIL: str


settings = Settings()
