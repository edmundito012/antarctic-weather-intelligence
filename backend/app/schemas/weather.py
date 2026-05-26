from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WeatherRecord(BaseModel):
    station: str
    datetime: datetime
    temperature: Optional[float] = None
    pressure: Optional[float] = None
    wind_speed: Optional[float] = None