from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

class EvaluationLabel(str, Enum):
    correct = "correct"
    partially_correct = "partialy_correct"
    incorrect = "incorrect"
    
class EvaluationRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    expected: str = Field(..., min_length=1)
    actual: str = Field(..., min_length=1)
    
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "prompt": "What is the capital of Argentina?",
                "expected": "Buenos Aires",
                "actual": "The capital of Argentina is Buenos Aires.",
            }
        },
    )
    
class EvaluationResponse(BaseModel):
    label: EvaluationLabel
    score: float = Field(..., ge=0.0, le=1.0)
    explanation: str = Field(..., min_length=1)
    
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "label": "correct",
                "score": 1.0,
                "explanation": "The actual answer matches the expected answer."
            }
        },
    )

class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"


class ErrorResponse(BaseModel):
    detail: str