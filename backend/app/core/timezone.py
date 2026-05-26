from datetime import datetime
from zoneinfo import ZoneInfo


MADRID_TIMEZONE = ZoneInfo("Europe/Madrid")


def convert_to_madrid_timezone(dt: datetime) -> datetime:
    """
    Convert datetime to Europe/Madrid timezone.
    """

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.astimezone(MADRID_TIMEZONE)