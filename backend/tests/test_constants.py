from app.core.constants import VALID_STATIONS


def test_valid_stations_include_required_stations():
    assert "gabriel" in VALID_STATIONS
    assert "juan" in VALID_STATIONS


def test_station_has_required_fields():
    station = VALID_STATIONS["gabriel"]

    assert station["name"] == "Gabriel de Castilla"
    assert isinstance(station["latitude"], float)
    assert isinstance(station["longitude"], float)