from datetime import datetime

from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/api/antarctica/data/start/{start_date}/end/{end_date}/station/{station_id}"
)
async def get_weather_data(
    start_date: str,
    end_date: str,
    station_id: str,
):
    parsed_start_date = datetime.fromisoformat(start_date)
    parsed_end_date = datetime.fromisoformat(end_date)

    return {
        "station": station_id,
        "start_date": parsed_start_date,
        "end_date": parsed_end_date,
        "message": "Endpoint is working correctly",
    }