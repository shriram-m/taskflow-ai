
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Explicitly load .env from project root
env_path = Path(__file__).parent / '.env'
print(f"Loading .env from: {env_path}")
print(f".env exists: {env_path.exists()}")

# Load environment variables
load_dotenv(env_path, override=True)

# Debug: Print what we loaded
loaded_key = os.getenv("GEMINI_API_KEY")
print(f"GEMINI_API_KEY loaded: {'Yes' if loaded_key else 'No'}")

class Settings(BaseSettings):
    # ADK & LLM Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    ADK_PROJECT_ID: str = os.getenv("ADK_PROJECT_ID", "taskflow-ai")
    
    # Vikunja Configuration
    VIKUNJA_URL: str = os.getenv("VIKUNJA_URL", "http://localhost:3456")
    VIKUNJA_USERNAME: str = os.getenv("VIKUNJA_USERNAME", "")
    VIKUNJA_PASSWORD: str = os.getenv("VIKUNJA_PASSWORD", "")
    VIKUNJA_PROJECT_ID: int = int(os.getenv("VIKUNJA_PROJECT_ID", "1"))
    
    # Voice Configuration
    VOICE_MODE: str = os.getenv("VOICE_MODE", "mock")
    VOICE_SERVICE: str = os.getenv("VOICE_SERVICE", "whisper")
    WHISPER_API_KEY: str = os.getenv("WHISPER_API_KEY", "")
    
    # Logging & Observability
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    ENABLE_TRACING: bool = os.getenv("ENABLE_TRACING", "false").lower() == "true"
    JAEGER_AGENT_HOST: str = os.getenv("JAEGER_AGENT_HOST", "localhost")
    JAEGER_AGENT_PORT: int = int(os.getenv("JAEGER_AGENT_PORT", "6831"))
    
    # Session Configuration
    SESSION_TTL_SECONDS: int = int(os.getenv("SESSION_TTL_SECONDS", "3600"))
    MAX_MEMORY_ITEMS: int = int(os.getenv("MAX_MEMORY_ITEMS", "100"))
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Debug output
print(f"\n=== Config Loaded ===")
print(f"GEMINI_API_KEY: {'Set' if settings.GEMINI_API_KEY else 'NOT SET'}")
print(f"VIKUNJA_URL: {settings.VIKUNJA_URL}")
print(f"VOICE_MODE: {settings.VOICE_MODE}")
print(f"ENABLE_TRACING: {settings.ENABLE_TRACING}")
print(f"===================\n")