import os
from pathlib import Path
from dotenv import load_dotenv

# Automatically find root .env or backend .env
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_ENV = BASE_DIR.parent.parent / ".env"
LOCAL_ENV = BASE_DIR / ".env"

if ROOT_ENV.exists():
    load_dotenv(ROOT_ENV)
elif LOCAL_ENV.exists():
    load_dotenv(LOCAL_ENV)
else:
    load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
