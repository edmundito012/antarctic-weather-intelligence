from datetime import datetime as dt

from sqlalchemy import DateTime, Float, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class WeatherObservation(Base):
    __tablename__ = "weather_observations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    station_id: Mapped[str] = mapped_column(String, index=True)
    datetime: Mapped[dt] = mapped_column(DateTime, index=True)
    temperature: Mapped[float | None] = mapped_column(Float, nullable=True)
    pressure: Mapped[float | None] = mapped_column(Float, nullable=True)
    wind_speed: Mapped[float | None] = mapped_column(Float, nullable=True)
    source: Mapped[str] = mapped_column(String, default="open-meteo")
    created_at: Mapped[dt] = mapped_column(DateTime, default=dt.utcnow)

    __table_args__ = (
        UniqueConstraint("station_id", "datetime", name="uq_station_datetime"),
    )