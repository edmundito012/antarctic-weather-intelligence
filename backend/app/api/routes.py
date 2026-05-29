from datetime import datetime

import httpx
from fastapi import APIRouter, HTTPException

from app.core.constants import VALID_STATIONS
from app.core.timezone import convert_to_madrid_timezone
from app.services.weather_service import WeatherService

router = APIRouter()


@router.get(
    "/api/antarctica/data/start/{start_date}/end/{end_date}/station/{station_id}"
)
async def get_weather_data(
    start_date: str,
    end_date: str,
    station_id: str,
):
    try:
        parsed_start_date = datetime.fromisoformat(start_date)
        parsed_end_date = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid datetime format. Use ISO format: YYYY-MM-DDTHH:MM:SS",
        )

    if parsed_start_date >= parsed_end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date must be earlier than end date",
        )

    station_key = station_id.lower()

    if station_key not in VALID_STATIONS:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid station. Valid stations: {list(VALID_STATIONS.keys())}",
        )

    madrid_start_date = convert_to_madrid_timezone(parsed_start_date)
    madrid_end_date = convert_to_madrid_timezone(parsed_end_date)

    weather_service = WeatherService()

    try:
        weather_data = await weather_service.fetch_weather_data(
            latitude=-62.97,
            longitude=-60.67,
            start_date=parsed_start_date.date().isoformat(),
            end_date=parsed_end_date.date().isoformat(),
        )
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Weather provider request failed: {str(exc)}",
        )

    return {
        "station": VALID_STATIONS[station_key],
        "start_date": madrid_start_date,
        "end_date": madrid_end_date,
        "message": "Weather data retrieved successfully",
        "source": "Open-Meteo Historical API",
        "weather_data": weather_data,
    }