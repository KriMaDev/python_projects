# Weather Forecast

Asks three weather services for the current weather in a city, prints each report, shows where they
agree or disagree, and calculates the average. It can also compare today's hourly forecast from two of them.

Providers: [OpenWeather](https://openweathermap.org/api), [WeatherAPI](https://www.weatherapi.com/) and
[Weatherstack](https://weatherstack.com/). All three have a free plan.

| File | What it contains |
|---|---|
| `weather.py` | **Entry point**: arguments, prompts, overall flow |
| `openweather.py`, `weatherapi.py`, `weatherstack.py` | One module per provider: fetch the current weather and parse the response |
| `forecasts.py` | Hourly (and the unfinished daily) forecasts |
| `display.py` | Printing the reports, the comparison and the average |
| `api_client.py` | Shared request helper: timeout and error messages that never contain your API key |
| `config.py` | Loads the API keys from `.env` |

## Setup

1. From the repository root, with your virtual environment active (see the [main README](../README.md#setup)):

   ```bash
   pip install -r Weather_Forecast/requirements.txt
   ```

2. Create free API keys at the three providers (new OpenWeather keys can take up to 2 hours to activate).

3. Copy the example settings file and fill in your keys:

   ```bash
   cp Weather_Forecast/.env.example Weather_Forecast/.env       # macOS / Linux
   copy Weather_Forecast\.env.example Weather_Forecast\.env     # Windows
   ```

   ```ini
   OPENWEATHER_API_KEY=your_key_here
   WEATHERAPI_API_KEY=your_key_here
   WEATHERSTACK_API_KEY=your_key_here
   WEATHERSTACK_HTTPS=0
   ```

   `.env` is in `.gitignore`, so your keys are never committed. The script finds it in `Weather_Forecast/` or in
   the repository root. If a key is missing, that provider is skipped with a message telling you which key to set.

## How to run

```bash
python Weather_Forecast/weather.py                       # asks for the city and the hourly forecast
python Weather_Forecast/weather.py Brussels              # asks only about the hourly forecast
python Weather_Forecast/weather.py Brussels --hourly     # current weather and hourly comparison
python Weather_Forecast/weather.py "New York" --no-hourly
python Weather_Forecast/weather.py --help
```

Every run uses 3 API calls, plus 2 more for the hourly forecast.

## Example output

Shortened. The numbers are sample data, so yours will differ:

```text
| Weather forecast for Brussels at 20/10/2026 12:21:09 |

| Selected data from all sources used for the report |

        | OpenWeather |

Condition         : Drizzle
Temperature       : 12.3 °C
Feels Like        : 11.0 °C
Humidity          : 80 %
Sea Pressure      : 1015 hPa
Visibility        : 8.0 km
Wind Speed        : 18.00 km/h
Rain              : True

        | WeatherAPI |
...
        | Data Comparing |

The forecasts disagree on rain status!
The forecasts show different conditions!
The temperature difference is 0.70°C between the forecasts.
The humidity difference is 4.00% between the forecasts.

        | Average Forecast |

Temperature            : 12.77 °C
Humidity               : 77.67 %
Pressure               : 1014.33 mbar (hPa)
Wind Speed             : 15.70 km/h
Visibility             : 9.33 km
Condition statuses are : | Drizzle | Partly cloudy | Light rain |
Statuses for rain are  : | True | False | True |
```

If a key is missing or wrong:

```text
WEATHERSTACK_API_KEY is not set. Copy Weather_Forecast/.env.example to .env and add your key.
ERROR_00: Fetching from OpenWeather: HTTP 401: Invalid API key. Please see https://openweathermap.org/faq#error401 for more info.
```

## Security note: Weatherstack uses HTTP

OpenWeather and WeatherAPI are called over **HTTPS**. Weatherstack's free plan does not support HTTPS, so its
key is sent **unencrypted**. Someone on the same network (for example public Wi-Fi) could read it. The risk is
small: a free key isn't linked to payment details, and the worst case is that someone uses up your monthly
quota. If you have a paid Weatherstack plan, set `WEATHERSTACK_HTTPS=1` in `.env`.

Error messages from `api_client.py` never include the request URL, because the URL contains the API key.

## Planned

- Compare tomorrow's forecast. `fetch_daily_forecasts()` is ready, but OpenWeather's daily data needs a
  separate One Call 3.0 subscription.
- Compare two cities in one run
- Add AccuWeather as a fourth provider

## Libraries

| Package | Used for | Licence |
|---|---|---|
| [requests](https://pypi.org/project/requests/) | HTTP calls to the weather APIs | Apache-2.0 |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Loading API keys from `.env` | BSD-3-Clause |
| [colorama](https://pypi.org/project/colorama/) | Coloured output on Windows | BSD-3-Clause |

Weather data © OpenWeather, WeatherAPI.com and Weatherstack. Each provider's terms of use apply to its data.
