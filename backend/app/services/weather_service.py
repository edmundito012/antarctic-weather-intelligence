from datetime import datetime
from statistics import mean

from loguru import logger

from app.models.weather_observation import WeatherObservation
from app.services.open_meteo_client import OpenMeteoClient


class WeatherService:
    def __init__(self, db):
        self.db = db
        self.weather_client = OpenMeteoClient()

    async def fetch_weather_data(
        self,
        station_id: str,
        latitude: float,
        longitude: float,
        start_date: datetime,
        end_date: datetime,
        aggregation: str = "none",
    ) -> dict:
        start_date = self._to_naive_datetime(start_date)
        end_date = self._to_naive_datetime(end_date)

        cached_records = self._get_cached_records(station_id, start_date, end_date)

        if cached_records:
            logger.info("Cache hit")
            records = cached_records if aggregation in {"none", "hourly"} else self._aggregate_records(cached_records, aggregation)
            return {"cache_status": "hit", "records": records}

        logger.info("Cache miss")
        logger.info("Calling Open-Meteo")

        raw_data = await self.weather_client.get_historical_weather_data(
            latitude=latitude,
            longitude=longitude,
            start_date=start_date.date().isoformat(),
            end_date=end_date.date().isoformat(),
        )

        records_to_save = self._normalize_open_meteo_response(station_id, raw_data)
        self._save_records(records_to_save)

        records = self._serialize_records(records_to_save)
        records = records if aggregation in {"none", "hourly"} else self._aggregate_records(records, aggregation)

        return {"cache_status": "miss", "records": records}

    def _get_cached_records(self, station_id: str, start_date: datetime, end_date: datetime) -> list[dict]:
        results = (
            self.db.query(WeatherObservation)
            .filter(
                WeatherObservation.station_id == station_id,
                WeatherObservation.datetime >= start_date,
                WeatherObservation.datetime <= end_date,
            )
            .order_by(WeatherObservation.datetime.asc())
            .all()
        )

        return [
            {
                "datetime": row.datetime.isoformat(timespec="minutes"),
                "temperature": row.temperature,
                "pressure": row.pressure,
                "wind_speed": row.wind_speed,
            }
            for row in results
        ]

    def _normalize_open_meteo_response(self, station_id: str, raw_data: dict) -> list[dict]:
        hourly = raw_data.get("hourly", {})
        times = hourly.get("time", [])
        temperatures = hourly.get("temperature_2m", [])
        pressures = hourly.get("surface_pressure", [])
        wind_speeds = hourly.get("wind_speed_10m", [])

        records = []

        for index, timestamp in enumerate(times):
            records.append(
                {
                    "station_id": station_id,
                    "datetime": datetime.fromisoformat(timestamp),
                    "temperature": temperatures[index] if index < len(temperatures) else None,
                    "pressure": pressures[index] if index < len(pressures) else None,
                    "wind_speed": wind_speeds[index] if index < len(wind_speeds) else None,
                }
            )

        return records

    def _save_records(self, records: list[dict]) -> None:
        try:
            for record in records:
                exists = (
                    self.db.query(WeatherObservation)
                    .filter(
                        WeatherObservation.station_id == record["station_id"],
                        WeatherObservation.datetime == record["datetime"],
                    )
                    .first()
                )

                if exists:
                    continue

                self.db.add(
                    WeatherObservation(
                        station_id=record["station_id"],
                        datetime=record["datetime"],
                        temperature=record["temperature"],
                        pressure=record["pressure"],
                        wind_speed=record["wind_speed"],
                        source="open-meteo",
                    )
                )

            self.db.commit()

        except Exception:
            self.db.rollback()
            logger.exception("Error saving weather records")
            raise

    def _serialize_records(self, records: list[dict]) -> list[dict]:
        serialized = []

        for record in records:
            dt = record["datetime"]
            if isinstance(dt, datetime):
                dt = dt.isoformat(timespec="minutes")

            serialized.append(
                {
                    "datetime": dt,
                    "temperature": record["temperature"],
                    "pressure": record["pressure"],
                    "wind_speed": record["wind_speed"],
                }
            )

        return serialized

    def _aggregate_records(self, records: list[dict], aggregation: str) -> list[dict]:
        grouped_records = {}

        for record in records:
            dt = datetime.fromisoformat(record["datetime"])

            if aggregation == "daily":
                key = dt.date().isoformat()
            elif aggregation == "monthly":
                key = f"{dt.year:04d}-{dt.month:02d}"
            else:
                raise ValueError("Invalid aggregation. Use: none, hourly, daily, monthly")

            grouped_records.setdefault(key, []).append(record)

        return [
            {
                "datetime": key,
                "temperature": self._average(group, "temperature"),
                "pressure": self._average(group, "pressure"),
                "wind_speed": self._average(group, "wind_speed"),
                "records_count": len(group),
            }
            for key, group in grouped_records.items()
        ]

    def _average(self, records: list[dict], field: str) -> float | None:
        values = [record[field] for record in records if record[field] is not None]
        return round(mean(values), 2) if values else None

    def _to_naive_datetime(self, dt: datetime) -> datetime:
        return dt.replace(tzinfo=None)