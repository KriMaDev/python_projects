import pytest
import requests

import api_client
from api_client import ApiError, error_message, get_json
from config import has_key
from forecasts import pair_hourly_forecasts
from openweather import parse_openweather
from weather import parse_yes_no
from weatherapi import parse_weatherapi
from weatherstack import parse_weatherstack

# Trimmed down real responses, only the fields the parsers use

OPENWEATHER_RESPONSE = {
    "weather": [{"main": "Drizzle"}],
    "main": {"temp": 12.3, "feels_like": 11.0, "temp_min": 10.0, "temp_max": 14.0,
             "humidity": 80, "sea_level": 1015, "grnd_level": 1010},
    "visibility": 8000,
    "wind": {"speed": 5},
}

WEATHERAPI_RESPONSE = {
    "location": {"region": "Brussels", "country": "Belgium", "lat": 50.83, "lon": 4.33, "localtime": "2026-10-20 12:00"},
    "current": {"temp_c": 13.0, "feelslike_c": 12.0, "humidity": 77, "windchill_c": 11.5, "wind_kph": 15.1,
                "wind_degree": 220, "wind_dir": "SW", "gust_kph": 25.0, "pressure_mb": 1014, "pressure_in": 29.94,
                "vis_km": 10, "uv": 2, "condition": {"text": "Partly cloudy"}},
}

WEATHERSTACK_RESPONSE = {
    "location": {"lat": "50.833", "lon": "4.333"},
    "current": {"temperature": 13, "feelslike": 12, "humidity": 76, "pressure": 1014, "wind_speed": 14,
                "wind_degree": 220, "wind_dir": "SW", "visibility": 10, "uv_index": 2,
                "weather_descriptions": ["Light rain"]},
}


def test_parse_openweather_converts_units():
    weather = parse_openweather(OPENWEATHER_RESPONSE)
    assert weather["vision"] == 8          # m -> km
    assert weather["w_spd"] == pytest.approx(18)  # m/s -> km/h
    assert weather["temp"] == 12.3
    assert weather["rain"] is True         # Drizzle counts as rain


def test_parse_weatherapi():
    weather = parse_weatherapi(WEATHERAPI_RESPONSE)
    assert weather["country"] == "Belgium"
    assert weather["mbar_p"] == 1014
    assert weather["condition"] == "Partly cloudy"
    assert weather["rain"] is False


def test_parse_weatherstack():
    weather = parse_weatherstack(WEATHERSTACK_RESPONSE)
    assert weather["temp"] == 13
    assert weather["rain"] is True


def test_parse_weatherstack_error_response():
    error = {"success": False, "error": {"code": 101, "info": "You have not supplied a valid API Access Key."}}
    with pytest.raises(ApiError, match="valid API Access Key"):
        parse_weatherstack(error)


@pytest.mark.parametrize(("answer", "expected"), [
    ("yes", True), ("Y", True), (" 1 ", True), ("True", True),
    ("no", False), ("N", False), ("0", False),
    ("maybe", None), ("", None),
])
def test_parse_yes_no(answer, expected):
    assert parse_yes_no(answer) is expected


@pytest.mark.parametrize(("data", "expected"), [
    ({"cod": 401, "message": "Invalid API key"}, "Invalid API key"),           # OpenWeather
    ({"error": {"code": 2006, "message": "API key is invalid."}}, "API key is invalid."),  # WeatherAPI
    ({"error": {"info": "Bad key"}}, "Bad key"),                               # Weatherstack
    ("not a dict", "unknown error"),
])
def test_error_message(data, expected):
    assert error_message(data) == expected


def test_get_json_never_leaks_the_api_key(monkeypatch):
    def fake_get(url, params, timeout):
        # requests includes the full URL with the query string in its error messages
        raise requests.exceptions.ConnectionError(f"Max retries exceeded with url: {url}?appid={params['appid']}")

    monkeypatch.setattr(api_client.requests, "get", fake_get)
    with pytest.raises(ApiError) as excinfo:
        get_json("https://example.com/weather", {"appid": "SECRET123"})
    assert "SECRET123" not in str(excinfo.value)


def test_has_key_explains_missing_key(capsys):
    assert has_key("OPENWEATHER_API_KEY", "abc") is True
    assert has_key("OPENWEATHER_API_KEY", "") is False
    assert ".env.example" in capsys.readouterr().out


# ---------------------------------------------------------------- hourly forecast pairing

NOW  = 1_800_000_000  # a whole hour in UTC
HOUR = 3600


def wapi_hours(offset=0):
    """48 WeatherAPI hours starting 10 hours ago, shifted by offset seconds (the city's time zone)."""
    return [{"time_epoch": NOW + (i - 10) * HOUR + offset, "time": f"local-{i}", "temp_c": 10.0, "condition": {"text": "Sunny"},
             "wind_kph": 20.0, "humidity": 60, "pressure_mb": 1010} for i in range(48)]


def openw_slots():
    """5 days of OpenWeather 3-hour slots starting now."""
    return [{"dt": NOW + i * 3 * HOUR, "dt_txt": f"utc-{i}", "main": {"temp": 12.0, "humidity": 70, "pressure": 1012},
             "weather": [{"description": "clear sky"}], "wind": {"speed": 5}} for i in range(40)]


def test_pair_hourly_forecasts_matches_on_timestamp():
    pairs = pair_hourly_forecasts(wapi_hours(), openw_slots(), now=NOW)

    assert len(pairs) == 9  # slots at +0h, +3h, ... +24h
    for wapi, openw in pairs:
        assert wapi["epoch"] == openw["epoch"]
    assert pairs[1][0]["time"] == "local-13"  # 10 hours back + 3 hours ahead


def test_pair_hourly_forecasts_converts_openweather_wind_to_kmh():
    wapi, openw = pair_hourly_forecasts(wapi_hours(), openw_slots(), now=NOW)[0]
    assert openw["wind_kph"] == pytest.approx(18)  # 5 m/s
    assert wapi["wind_kph"] == 20.0


def test_pair_hourly_forecasts_handles_half_hour_time_zones():
    pairs = pair_hourly_forecasts(wapi_hours(offset=30 * 60), openw_slots(), now=NOW)
    assert len(pairs) == 9


def test_pair_hourly_forecasts_skips_times_too_far_apart():
    # A single WeatherAPI hour exactly between two OpenWeather slots (1.5 hours from both)
    lonely_hour = [hour for hour in wapi_hours(offset=30 * 60) if hour["time_epoch"] == NOW + 90 * 60]
    assert len(lonely_hour) == 1
    assert pair_hourly_forecasts(lonely_hour, openw_slots(), now=NOW) == []


def test_pair_hourly_forecasts_without_weatherapi_data():
    assert pair_hourly_forecasts([], openw_slots(), now=NOW) == []
