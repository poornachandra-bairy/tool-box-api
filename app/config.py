from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama3-8b-8192")
    MODEL_ENDPOINT: str = os.getenv("MODEL_ENDPOINT", "https://api.groq.com/openai/v1/chat/completions")
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True

# Print environment variables for debugging
print("Current working directory:", os.getcwd())
env_path = os.path.join(os.getcwd(), ".env")
print("Environment file path:", env_path)
print("File exists:", os.path.exists(env_path))
print("GROQ_API_KEY in environment:", os.getenv("GROQ_API_KEY"))

settings = Settings()
print("Loaded GROQ_API_KEY:", settings.GROQ_API_KEY)
