from pydantic_settings import BaseSettings
from urllib.parse import unquote

class Settings(BaseSettings):
    RAW_DATABASE_URL: str
    DEBUG: bool

    @property
    def DATABASE_URL(self) -> str:
        return unquote(self.RAW_DATABASE_URL)

    class Config:
        env_file = ".env"

settings = Settings()
