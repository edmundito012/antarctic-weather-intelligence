from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_invalid_station_returns_404():
    response = client.get(
        "/api/antarctica/data/start/2024-01-01T00:00:00/end/2024-01-02T00:00:00/station/invalid"
    )

    assert response.status_code == 404
    assert "Invalid station" in response.json()["detail"]


def test_invalid_aggregation_returns_400():
    response = client.get(
        "/api/antarctica/data/start/2024-01-01T00:00:00/end/2024-01-02T00:00:00/station/gabriel?aggregation=weekly"
    )

    assert response.status_code == 400
    assert "Invalid aggregation" in response.json()["detail"]


def test_invalid_date_returns_400():
    response = client.get(
        "/api/antarctica/data/start/bad-date/end/2024-01-02T00:00:00/station/gabriel"
    )

    assert response.status_code == 400
    assert "Invalid datetime format" in response.json()["detail"]


def test_start_date_after_end_date_returns_400():
    response = client.get(
        "/api/antarctica/data/start/2024-01-10T00:00:00/end/2024-01-01T00:00:00/station/gabriel"
    )

    assert response.status_code == 400
    assert "Start date must be earlier" in response.json()["detail"]