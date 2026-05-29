import httpx

from app.core.config import settings


class AemetClient:
    BASE_URL = "https://opendata.aemet.es/opendata/api"

    async def get_weather_data(
        self,
        start_date: str,
        end_date: str,
        station_id: str,
    ):
        endpoint = (
            f"{self.BASE_URL}/observacion/convencional/"
            f"datos/fechaini/{start_date}/fechafin/{end_date}/estacion/{station_id}"
        )

        headers = {
            "api_key": settings.AEMET_API_KEY,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(endpoint, headers=headers)

            response.raise_for_status()

            return response.json()