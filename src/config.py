# config file for the project

import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")

SEARCHES = int(os.getenv("SEARCHES", "20"))  # Default to 20 searches
