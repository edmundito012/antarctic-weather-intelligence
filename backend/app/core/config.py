import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    AEMET_API_KEY = os.getenv("AEMET_API_KEY")


settings = Settings()