from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.evaluator.llm_evaluator import evaluate

from src.schemas import (
    ErrorResponse,
    EvaluationRequest,
    EvaluationResponse,
    HealthResponse,
)

app = FastAPI(title="LLM Test Evaluator API")

@app.exception_handler(ValueError)
async def value_error_handler(_: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(detail=str(exc)).model_dump(),
    )
    
@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(detail="Internal server error").model_dump(),
    )

@app.get("/health", response_model=HealthResponse, tags=["system"])
def health():
    return HealthResponse


@app.post(
    "/evaluate",
    response_model=EvaluationResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    tags=["evaluation"]
    )
def evaluate_endpoint(payload: EvaluationRequest) -> EvaluationResponse:
    return evaluate(
            prompt=payload.prompt,
            expected=payload.expected,
            actual=payload.actual,
        )