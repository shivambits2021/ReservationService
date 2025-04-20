import urllib.parse
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG :bool

    def get_database_url(self):
        return urllib.parse.unquote(self.DATABASE_URL)

    class Config:
        env_file = ".env"

settings = Settings()
settings.DATABASE_URL = settings.get_database_url()
