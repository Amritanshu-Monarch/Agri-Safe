from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # OpenWeatherMap API
    OPENWEATHER_API_KEY: str = "your_openweather_api_key_here"

    # Google Gemini API (for RAG chatbot)
    GEMINI_API_KEY: str = "your_gemini_api_key_here"

    # Path to your trained CNN model (.h5 or .tflite)
    MODEL_PATH: str = "app/models/crop_disease_model.h5"

    # Path to agriculture knowledge base PDF/text for RAG
    KNOWLEDGE_BASE_PATH: str = "app/data/agriculture_manual.pdf"

    # Confidence threshold for disease detection
    CONFIDENCE_THRESHOLD: float = 0.70

    # Rain probability threshold (%) - above this we say "wait to spray"
    RAIN_THRESHOLD_PERCENT: int = 40

    class Config:
        env_file = ".env"

settings = Settings()
