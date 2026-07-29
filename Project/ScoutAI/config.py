"""
SmartScout Configuration
"""

from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

(BASE_DIR / "data").mkdir(parents=True, exist_ok=True)
(BASE_DIR / "data" / "cache").mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

   

    APP_NAME: str = "SmartScout"
    VERSION: str = "1.0.0"
    DEBUG: bool = True



    DATABASE_URL: str = "sqlite:///./data/jobs.db"



    GROQ_API_KEY: str = ""

    # llama-3.3-70b-versatile was deprecated by Groq (announced
    # June 17, 2026); openai/gpt-oss-120b is Groq's recommended
    # replacement for that model.
    GROQ_MODEL: str = "openai/gpt-oss-120b"



    EMBEDDING_MODEL: str = "BAAI/bge-large-en-v1.5"



    GOOGLE_API_KEY: str = ""
    GOOGLE_CSE_ID: str = ""



    MAX_SEARCH_RESULTS: int = 20

    REQUEST_TIMEOUT: int = 30

    USER_AGENT: str = (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )


    TOP_MATCHES: int = 10
    MIN_MATCH_SCORE: float = 0.60



    MAX_RESUME_SIZE_MB: int = 10

    ALLOWED_FILE_TYPES: list[str] = [
        "pdf",
        "docx",
        "txt"
    ]



    ENABLE_CACHE: bool = True

    CACHE_DIRECTORY: str = "./data/cache"



    LOG_LEVEL: str = "INFO"



    FRONTEND_URL: str = "http://localhost:3000"


settings = Settings()