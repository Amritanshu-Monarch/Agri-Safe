"""
Weather Advisory Service
────────────────────────
Fetches the 3-hour forecast from OpenWeatherMap for the next 12 hours.
Determines rain probability to inform spray decisions.
"""
import httpx
from app.config import settings


async def get_weather_advisory(lat: float, lon: float) -> dict:
    """
    Calls OpenWeatherMap 5-day/3-hour forecast API.
    Returns a summary with:
     - current conditions
     - rain probability in next 12 hours
     - wind speed
     - humidity
     - advisory flag: rain_expected (bool)
    """
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": settings.OPENWEATHER_API_KEY,
        "units": "metric",
        "cnt": 4,  # Next 4 intervals = 12 hours (3h each)
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPStatusError as e:
        # If API key is missing or invalid, return a mock response for development
        print(f"⚠️  Weather API error: {e} — using mock data.")
        return _mock_weather()
    except Exception as e:
        print(f"⚠️  Weather fetch failed: {e} — using mock data.")
        return _mock_weather()

    forecasts = data.get("list", [])
    if not forecasts:
        return _mock_weather()

    # Aggregate rain probability across next 12 hours
    max_rain_prob   = max(f.get("pop", 0) for f in forecasts) * 100  # pop is 0.0–1.0
    avg_humidity    = sum(f["main"]["humidity"] for f in forecasts) / len(forecasts)
    avg_wind_speed  = sum(f["wind"]["speed"] for f in forecasts) / len(forecasts)
    current         = forecasts[0]
    weather_desc    = current["weather"][0]["description"].title()
    temp            = current["main"]["temp"]

    rain_expected   = max_rain_prob >= settings.RAIN_THRESHOLD_PERCENT

    return {
        "current_condition": weather_desc,
        "temperature_c": round(temp, 1),
        "humidity_percent": round(avg_humidity, 1),
        "wind_speed_kmh": round(avg_wind_speed * 3.6, 1),  # m/s to km/h
        "rain_probability_percent": round(max_rain_prob, 1),
        "rain_expected_12h": rain_expected,
        "source": "OpenWeatherMap",
    }


def _mock_weather() -> dict:
    """Fallback mock weather data for development/testing."""
    return {
        "current_condition": "Partly Cloudy",
        "temperature_c": 26.5,
        "humidity_percent": 72.0,
        "wind_speed_kmh": 12.0,
        "rain_probability_percent": 65.0,
        "rain_expected_12h": True,
        "source": "mock",
    }
