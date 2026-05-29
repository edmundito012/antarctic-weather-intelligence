from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WeatherRecord(BaseModel):
    datetime: str
    temperature: Optional[float] = None
    pressure: Optional[float] = None
    wind_speed: Optional[float] = None


class AggregatedWeatherRecord(WeatherRecord):
    records_count: int


class WeatherResponse(BaseModel):
    station: str
    station_id: str
    start_date: datetime
    end_date: datetime
    aggregation: str
    cache_status: str
    records_count: int
    records: list[WeatherRecord | AggregatedWeatherRecord]