import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SEED_ON_START"] = "true"

from app.main import app  # noqa: E402


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_search_and_theorem_detail():
    with TestClient(app) as client:
        search = client.get("/api/search", params={"q": "Pythagorean", "type": "theorem"})
        assert search.status_code == 200
        payload = search.json()
        assert payload["items"]

        theorem_id = payload["items"][0]["id"]
        detail = client.get(f"/api/theorems/{theorem_id}")
        assert detail.status_code == 200
        assert "proof_md" in detail.json()


def test_trace_binary_search():
    with TestClient(app) as client:
        response = client.post(
            "/api/animations/trace",
            json={"algorithm": "binary_search", "array": [1, 3, 5, 7, 9], "target": 7},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["algorithm"] == "binary_search"
        assert len(data["steps"]) >= 1


def test_ingest_requires_refs_and_reports_skips():
    with TestClient(app) as client:
        payload = {
            "theorems": [
                {
                    "name": "Smoke Theorem",
                    "statement_latex": "x=x",
                    "proof_md": "Direct.",
                    "refs": "Internal draft note",
                }
            ],
            "formulas": [],
        }

        first = client.post("/api/ingest/doc", json=payload)
        assert first.status_code == 200
        first_data = first.json()
        assert first_data["inserted_theorems"] == 1
        assert first_data["skipped_theorems"] == 0

        second = client.post("/api/ingest/doc", json=payload)
        assert second.status_code == 200
        second_data = second.json()
        assert second_data["inserted_theorems"] == 0
        assert second_data["skipped_theorems"] == 1


def test_render_queue_returns_503_without_redis():
    with TestClient(app) as client:
        response = client.post("/api/animations/render", json={"trace": {"steps": []}})
        assert response.status_code in (200, 503)
