from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.db.database import Base, engine
from app.models.weather_observation import WeatherObservation

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Antarctic Weather Intelligence API",
    description=(
        "FastAPI service for Antarctic historical weather data, "
        "aggregation, SQLite caching and dashboard visualization."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def root():
    return {
        "message": "Antarctic Weather Intelligence API is running",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "antarctic-weather-intelligence",
        "version": "1.0.0",
    }