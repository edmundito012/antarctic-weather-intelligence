from datetime import datetime

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.constants import VALID_STATIONS
from app.core.timezone import convert_to_madrid_timezone
from app.db.database import get_db
from app.schemas.weather import WeatherResponse
from app.services.weather_service import WeatherService

router = APIRouter()

VALID_AGGREGATIONS = {"none", "hourly", "daily", "monthly"}
VALID_FIELDS = {"temperature", "pressure", "wind_speed"}


@router.get(
    "/api/antarctica/data/start/{start_date}/end/{end_date}/station/{station_id}",
    response_model=WeatherResponse,
    response_model_exclude_none=True,
)
async def get_weather_data(
    start_date: str,
    end_date: str,
    station_id: str,
    aggregation: str = Query(
        default="none",
        description="Aggregation type: none, hourly, daily, monthly",
    ),
    fields: str | None = Query(
        default=None,
        description="Optional fields: temperature, pressure, wind_speed",
    ),
    db: Session = Depends(get_db),
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

    aggregation = aggregation.lower()

    if aggregation not in VALID_AGGREGATIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid aggregation. Use: none, hourly, daily, monthly",
        )

    selected_fields = None

    if fields:
        selected_fields = [field.strip() for field in fields.split(",")]

        invalid_fields = [
            field for field in selected_fields if field not in VALID_FIELDS
        ]

        if invalid_fields:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid fields. Use any combination of: "
                    "temperature, pressure, wind_speed"
                ),
            )

    station_key = station_id.lower()

    if station_key not in VALID_STATIONS:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid station. Valid stations: {list(VALID_STATIONS.keys())}",
        )

    madrid_start_date = convert_to_madrid_timezone(parsed_start_date)
    madrid_end_date = convert_to_madrid_timezone(parsed_end_date)
    station = VALID_STATIONS[station_key]

    weather_service = WeatherService(db=db)

    try:
        weather_data = await weather_service.fetch_weather_data(
            station_id=station_key,
            latitude=station["latitude"],
            longitude=station["longitude"],
            start_date=madrid_start_date,
            end_date=madrid_end_date,
            aggregation=aggregation,
            fields=selected_fields,
        )
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Weather provider request failed: {str(exc)}",
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return {
        "station": station["name"],
        "station_id": station_key,
        "start_date": madrid_start_date.isoformat(),
        "end_date": madrid_end_date.isoformat(),
        "aggregation": aggregation,
        "cache_status": weather_data["cache_status"],
        "records_count": len(weather_data["records"]),
        "records": weather_data["records"],
    }