import os
from dotenv import load_dotenv, find_dotenv

# Attempt to find and load the .env file
env_file = find_dotenv(usecwd=True)
if env_file:
    load_dotenv(env_file)

class Settings:
    # Application settings
    APP_NAME = os.getenv("APP_NAME", "workoutapp.ai")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Database settings
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///default.db")

    # API settings
    MODEL_NAME=os.getenv("MODEL_NAME")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    API_PROVIDER = os.getenv("API_PROVIDER")
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Environment-specific settings
    ENV = os.getenv("ENV", "development")

    if ENV == "production":
        # Production-specific settings
        DEBUG = False
        LOG_LEVEL = "ERROR"
    elif ENV == "staging":
        # Staging-specific settings
        DEBUG = True
        LOG_LEVEL = "WARNING"
    else:
        # Development-specific settings
        DEBUG = True
        LOG_LEVEL = "DEBUG"


    # Other settings
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

# Create a single instance of Settings
settings = Settings()

