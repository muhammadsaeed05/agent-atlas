from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_travel_endpoint():
    response = client.post("/api/travel", json={"message": "Plan a 3 day trip to Tokyo"})
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
