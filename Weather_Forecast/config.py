"""API keys and settings for the weather providers, loaded from a .env file."""
import os
from pathlib import Path

from colorama import Fore
from dotenv import load_dotenv

# Real environment variables win, then Weather_Forecast/.env, then .env in the repository root
TOOL_DIR = Path(__file__).resolve().parent
load_dotenv(TOOL_DIR / ".env")
load_dotenv(TOOL_DIR.parent / ".env")

OPENWEATHER_API_KEY  = os.getenv("OPENWEATHER_API_KEY", "").strip()
WEATHERAPI_API_KEY   = os.getenv("WEATHERAPI_API_KEY", "").strip()
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY", "").strip()

# Weatherstack's free plan only accepts HTTP. Set WEATHERSTACK_HTTPS=1 on a paid plan.
WEATHERSTACK_HTTPS = os.getenv("WEATHERSTACK_HTTPS", "0").strip() == "1"

# Seconds to wait for an API before giving up
REQUEST_TIMEOUT = 10


def has_key(name: str, value: str) -> bool:
    """Return True if the key is set, otherwise print how to set it and return False."""
    if value:
        return True
    print(Fore.YELLOW + f"{name} is not set. Copy Weather_Forecast/.env.example to .env and add your key.")
    return False
