"""Small wrapper around requests for the weather APIs."""
from typing import Any

import requests

from config import REQUEST_TIMEOUT


class ApiError(Exception):
    """A weather API request failed. The message never contains the URL (it holds the API key)."""


def get_json(url: str, params: dict[str, Any]) -> Any:
    """GET a JSON API with a timeout and return the decoded response."""
    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.Timeout:
        raise ApiError(f"no answer within {REQUEST_TIMEOUT} seconds") from None
    except requests.exceptions.RequestException as e:
        # Don't print e itself: requests puts the full URL, including the key, in the message
        raise ApiError(f"connection failed ({type(e).__name__})") from None

    try:
        data = response.json()
    except ValueError:
        raise ApiError(f"HTTP {response.status_code}, response is not JSON") from None

    if not response.ok:
        raise ApiError(f"HTTP {response.status_code}: {error_message(data)}")
    return data


def error_message(data: Any) -> str:
    """Pull the human readable error out of an API error response."""
    if isinstance(data, dict):
        error = data.get("error")
        if isinstance(error, dict):
            return str(error.get("message") or error.get("info") or error)
        if data.get("message"):
            return str(data["message"])
    return "unknown error"
