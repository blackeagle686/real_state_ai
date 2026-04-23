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

    # Vector DB
    VECTOR_DB_TYPE: str = "chroma"
    CHROMA_PERSIST_DIR: str = "./chroma_db"

    # OpenAI / Long Cat
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.longcat.io/v1"

    # Features
    ENABLE_VLM: bool = False
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra='ignore')

settings = Settings()
