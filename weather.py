from fastapi import APIRouter
from app.services.weather_service import get_weather_advisory

router = APIRouter()

@router.get("/current")
async def get_current_weather(lat: float, lon: float):
    """
    Standalone weather endpoint for the frontend weather widget.
    """
    weather = await get_weather_advisory(lat, lon)
    return weather
