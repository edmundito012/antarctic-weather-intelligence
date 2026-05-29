from fastapi import FastAPI

from app.api.routes import router
from app.db.database import Base, engine
from app.models.weather_observation import WeatherObservation

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Antarctic Weather Intelligence",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "API is running"}