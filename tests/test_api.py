import src.api.main as api_main
from fastapi.testclient import TestClient

from src.schemas import EvaluationResponse

client = TestClient(api_main.app)
client_no_raise = TestClient(api_main.app, raise_server_exceptions=False)


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
    
def test_evaluate_returns_400_for_value_error(monkeypatch):
    def fake_evaluate(prompt: str, expected: str, actual: str):
        raise ValueError("Invalid evaluator output")

    monkeypatch.setattr(api_main, "evaluate", fake_evaluate)

    response = client.post(
        "/evaluate",
        json={
            "prompt": "What is the capital of France?",
            "expected": "Paris",
            "actual": "Paris",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid evaluator output"}


def test_evaluate_returns_500_for_unexpected_error(monkeypatch):
    def fake_evaluate(prompt: str, expected: str, actual: str):
        raise RuntimeError("unexpected boom")

    monkeypatch.setattr(api_main, "evaluate", fake_evaluate)

    response = client_no_raise.post(
        "/evaluate",
        json={
            "prompt": "What is the capital of France?",
            "expected": "Paris",
            "actual": "Paris",
        },
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}