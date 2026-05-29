from app.services.weather_service import WeatherService


def test_average_returns_rounded_average():
    service = WeatherService(db=None)

    records = [
        {"temperature": 1.0},
        {"temperature": 2.0},
        {"temperature": 3.0},
    ]

    result = service._average(records, "temperature")

    assert result == 2.0


def test_average_returns_none_when_values_missing():
    service = WeatherService(db=None)

    records = [
        {"temperature": None},
        {"temperature": None},
    ]

    result = service._average(records, "temperature")

    assert result is None


def test_aggregate_records_daily():
    service = WeatherService(db=None)

    records = [
        {
            "datetime": "2024-01-01T00:00",
            "temperature": 1.0,
            "pressure": 990.0,
            "wind_speed": 2.0,
        },
        {
            "datetime": "2024-01-01T01:00",
            "temperature": 3.0,
            "pressure": 994.0,
            "wind_speed": 4.0,
        },
    ]

    result = service._aggregate_records(records, "daily")

    assert len(result) == 1
    assert result[0]["datetime"] == "2024-01-01"
    assert result[0]["temperature"] == 2.0
    assert result[0]["pressure"] == 992.0
    assert result[0]["wind_speed"] == 3.0
    assert result[0]["records_count"] == 2