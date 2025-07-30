import os

class Settings:
    API_KEY: str = os.getenv("API_KEY", "dummy-api-key")

settings = Settings()
