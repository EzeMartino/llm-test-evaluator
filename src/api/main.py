from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict

from src.evaluator.llm_evaluator import evaluate

app = FastAPI(title="LLM Test Evaluator API")


class EvaluationInput(BaseModel):
    prompt: str
    expected: str
    actual: str

    model_config = ConfigDict(extra="forbid")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/evaluate")
def evaluate_endpoint(payload: EvaluationInput):
    try:
        result = evaluate(
            prompt=payload.prompt,
            expected=payload.expected,
            actual=payload.actual,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")