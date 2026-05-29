from datetime import datetime
from zoneinfo import ZoneInfo

from app.core.timezone import convert_to_madrid_timezone


def test_convert_naive_datetime_to_madrid_timezone():
    dt = datetime(2024, 1, 1, 0, 0, 0)

    result = convert_to_madrid_timezone(dt)

    assert result.tzinfo is not None
    assert result.isoformat() == "2024-01-01T01:00:00+01:00"


def test_convert_utc_datetime_to_madrid_timezone_summer_dst():
    dt = datetime(2024, 7, 1, 0, 0, 0, tzinfo=ZoneInfo("UTC"))

    result = convert_to_madrid_timezone(dt)

    assert result.isoformat() == "2024-07-01T02:00:00+02:00"