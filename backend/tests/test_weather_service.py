from datetime import datetime, timedelta, UTC

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


def test_aggregate_records_monthly():
    service = WeatherService(db=None)

    records = [
        {
            "datetime": "2024-01-01T00:00",
            "temperature": 1.0,
            "pressure": 990.0,
            "wind_speed": 2.0,
        },
        {
            "datetime": "2024-01-15T00:00",
            "temperature": 3.0,
            "pressure": 994.0,
            "wind_speed": 4.0,
        },
        {
            "datetime": "2024-02-01T00:00",
            "temperature": 5.0,
            "pressure": 998.0,
            "wind_speed": 6.0,
        },
    ]

    result = service._aggregate_records(records, "monthly")

    assert len(result) == 2
    assert result[0]["datetime"] == "2024-01"
    assert result[0]["temperature"] == 2.0
    assert result[0]["pressure"] == 992.0
    assert result[0]["wind_speed"] == 3.0
    assert result[0]["records_count"] == 2

    assert result[1]["datetime"] == "2024-02"
    assert result[1]["temperature"] == 5.0
    assert result[1]["pressure"] == 998.0
    assert result[1]["wind_speed"] == 6.0
    assert result[1]["records_count"] == 1


def test_filter_fields_returns_only_selected_fields():
    service = WeatherService(db=None)

    records = [
        {
            "datetime": "2024-01-01",
            "temperature": 1.0,
            "pressure": 990.0,
            "wind_speed": 2.0,
            "records_count": 24,
        }
    ]

    result = service._filter_fields(records, ["temperature"])

    assert result == [
        {
            "datetime": "2024-01-01",
            "temperature": 1.0,
            "records_count": 24,
        }
    ]


def test_calculate_cache_age_minutes_returns_value():
    service = WeatherService(db=None)

    records = [
        {
            "created_at": datetime.now(UTC) - timedelta(minutes=5)
        }
    ]

    result = service._calculate_cache_age_minutes(records)

    assert result is not None
    assert result >= 4.9