from app.services.open_meteo_client import OpenMeteoClient


class WeatherService:
    def __init__(self):
        self.weather_client = OpenMeteoClient()

    async def fetch_weather_data(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
    ) -> dict:
        return await self.weather_client.get_historical_weather_data(
            latitude=latitude,
            longitude=longitude,
            start_date=start_date,
            end_date=end_date,
        )