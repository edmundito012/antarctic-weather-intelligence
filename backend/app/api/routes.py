from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.core.constants import VALID_STATIONS

from app.core.timezone import convert_to_madrid_timezone

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

    if station_id.lower() not in VALID_STATIONS:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid station. Valid stations: {list(VALID_STATIONS.keys())}",
        )

    parsed_start_date = convert_to_madrid_timezone(parsed_start_date)
    parsed_end_date = convert_to_madrid_timezone(parsed_end_date)

    return {
        "station": VALID_STATIONS[station_id.lower()],
        "start_date": parsed_start_date,
        "end_date": parsed_end_date,
        "message": "Weather request validated successfully",
    }