import os
from pydantic import BaseModel

class Settings(BaseModel):
    DB_URL: str = os.getenv("DB_URL", "sqlite:///./books.db")

settings = Settings()
