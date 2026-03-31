import src.api.main as api_main
from fastapi.testclient import TestClient

from src.schemas import EvaluationResponse

client = TestClient(api_main.app)


def test_health_contract():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_evaluate_contract(monkeypatch):
    def fake_evaluate(prompt: str, expected: str, actual: str):
        return EvaluationResponse(
            label="correct",
            score=1.0,
            explanation="Exact match",
        )

    monkeypatch.setattr(api_main, "evaluate", fake_evaluate)

    response = client.post(
        "/evaluate",
        json={
            "prompt": "What is the capital of France?",
            "expected": "Paris",
            "actual": "Paris",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "label": "correct",
        "score": 1.0,
        "explanation": "Exact match",
    }


def test_evaluate_rejects_extra_fields():
    response = client.post(
        "/evaluate",
        json={
            "prompt": "What is the capital of France?",
            "expected": "Paris",
            "actual": "Paris",
            "extra_field": "should fail",
        },
    )

    assert response.status_code == 422