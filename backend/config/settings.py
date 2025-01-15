from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

class Settings(BaseSettings):
    """Application settings."""
    
    # Base Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DOCS_DIR: Path = BASE_DIR / "generated_docs"
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI DOCS GENERATOR"
    
    # Google Cloud Configuration
    GOOGLE_API_KEY: Optional[str] = None
    GOOGLE_PROJECT_ID: Optional[str] = None
    GOOGLE_LOCATION: str = "us-central1"  # Default region
    GEMINI_MODEL_NAME: str = "gemini-pro"  # Using gemini-pro instead of flash
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings() 