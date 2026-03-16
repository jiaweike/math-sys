import os

from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SEED_ON_START"] = "true"

from app.main import app  # noqa: E402


def test_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_search_and_theorem_detail():
    client = TestClient(app)

    search = client.get("/api/search", params={"q": "Pythagorean", "type": "theorem"})
    assert search.status_code == 200
    payload = search.json()
    assert payload["items"]

    theorem_id = payload["items"][0]["id"]
    detail = client.get(f"/api/theorems/{theorem_id}")
    assert detail.status_code == 200
    assert "proof_md" in detail.json()


def test_trace_binary_search():
    client = TestClient(app)
    response = client.post(
        "/api/animations/trace",
        json={"algorithm": "binary_search", "array": [1, 3, 5, 7, 9], "target": 7},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["algorithm"] == "binary_search"
    assert len(data["steps"]) >= 1
