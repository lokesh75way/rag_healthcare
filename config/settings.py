from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    google_api_key: str
    backend_api_url: str
    backend_api_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
