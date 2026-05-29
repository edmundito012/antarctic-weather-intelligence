from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WeatherRecord(BaseModel):
    datetime: datetime
    temperature: Optional[float] = None
    pressure: Optional[float] = None
    wind_speed: Optional[float] = None


class WeatherResponse(BaseModel):
    station: str
    station_id: str
    aggregation: str
    records_count: int
    records: list[WeatherRecord]