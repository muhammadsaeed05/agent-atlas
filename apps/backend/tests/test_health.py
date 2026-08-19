from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_travel_endpoint():
    with patch(
        "main.run_travel_workflow",
        new_callable=AsyncMock,
        return_value={
            "itinerary": "Tokyo Itinerary: Day 1 Shibuya, Day 2 Shinjuku",
            "flight_results": "Flight Info",
            "hotel_results": "Hotel Info",
            "weather_results": "Sunny 22C",
        },
    ):
        response = client.post("/api/travel", json={"message": "Plan a 3 day trip to Tokyo"})
        assert response.status_code == 200
        data = response.json()
        assert "reply" in data
