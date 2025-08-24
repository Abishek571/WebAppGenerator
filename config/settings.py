"""
Configuration loader using dotenv.
"""

import os
from dotenv import load_dotenv

load_dotenv()
FOLDER_PATH = "outputs"
class Config:
    ENV = os.getenv("ENV", "dev")
    DEBUG = ENV == "dev"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LOG_DIR = os.getenv("LOG_DIR", "./logs")
config = Config()