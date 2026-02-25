from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_ask_valid_question():
    response = client.post("/api/v1/ask", json={
        "question": "Como captar mais clientes pelo Instagram?",
        "max_results": 3
    })
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["answer"]) > 50
    assert isinstance(data["sources"], list)
    assert data["latency_ms"] > 0

def test_ask_empty_question():
    response = client.post("/api/v1/ask", json={"question": ""})
    assert response.status_code == 400