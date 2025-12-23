from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8001
    MODEL_PATH: str = "./models/sentiment_model.pkl"
    VECTORIZER_PATH: str = "./models/vectorizer.pkl"
    MIN_SAMPLES_FOR_ANALYSIS: int = 10
    
    class Config:
        env_file = ".env"

settings = Settings()
