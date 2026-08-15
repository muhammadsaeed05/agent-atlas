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
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY", "")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

# LangSmith Tracing
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY") or os.getenv("LANGCHAIN_API_KEY", "")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT") or os.getenv("LANGCHAIN_PROJECT", "agent-atlas")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false")

# LLM Gateway defaults
LLM_MODEL = os.getenv("LLM_MODEL", "openrouter/meta-llama/llama-3.3-70b-instruct")
LLM_FALLBACK_MODEL = os.getenv("LLM_FALLBACK_MODEL", "groq/llama-3.3-70b-versatile")
LLM_RETRIES = int(os.getenv("LLM_RETRIES", "2"))
LLM_TIMEOUT = float(os.getenv("LLM_TIMEOUT", "60.0"))
