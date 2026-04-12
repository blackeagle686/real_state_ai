from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Real-Time Arabic AI Assistant"
    VERSION: str = "0.1.0"
    
    DEEPGRAM_API_KEY: str = ""
    LONGCAT_API_KEY: str = ""
    ELEVENLABS_API_KEY: str = ""
    
    LONGCAT_BASE_URL: str = "https://api.longcat.io/v1"  # Replace with actual LongCat endpoint if different
    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
