import httpx


class OpenMeteoClient:
    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

    async def get_historical_weather_data(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
    ) -> dict:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": "temperature_2m,surface_pressure,wind_speed_10m",
            "wind_speed_unit": "ms",
            "timezone": "Europe/Madrid",
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()