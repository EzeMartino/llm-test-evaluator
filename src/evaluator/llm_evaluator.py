# from openai import OpenAI
import json
import re
from textwrap import dedent

from pydantic import ValidationError
from src.evaluator.providers import call_openai
from src.evaluator.rule_based import rule_based_evaluate
from src.config import USE_LLM, SYSTEM_PROMPT
from src.schemas import EvaluationResponse

    
# VALID_LABELS = {"correct", "partially_correct", "incorrect"}

def build_prompt(prompt, expected, actual):
    return dedent(
        f"""
        Prompt:
        {prompt}

        Expected Answer:
        {expected}

        Actual Answer:
        {actual}
    """
    ).strip()
    
def parse_response(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Invalid JSON response: {text}")
    
def validate_output(output):
    try:
        return EvaluationResponse.model_validate(output)
    except ValidationError as exc:
        raise ValueError("Invalid evaluator output") from exc

def evaluate(
    prompt: str, 
    expected: str, 
    actual: str, 
    use_LLM: bool | None = None
    ) -> EvaluationResponse:
    
    use_llm = USE_LLM if use_LLM is None else use_LLM

    if not use_llm:
        return rule_based_evaluate(expected, actual)
    
    user_prompt = build_prompt(prompt, expected, actual)
    
    try:
        raw_output = call_openai(SYSTEM_PROMPT, user_prompt)
        parsed = parse_response(raw_output)
        
        return validate_output(parsed)
    
    except Exception:
        # Automatic fallback if LLM fails
        fallback = rule_based_evaluate(expected, actual)
        return fallback.model_copy(
            update={
                "explanation": (
                    f"{fallback.explanation} "
                    "(Fallback used because the LLM evaluator was unavailable)"
                )
            }
        )

if __name__ == "__main__":
    result = evaluate(
        prompt="What is the capital of Argentina?",
        expected="Buenos Aires",
        actual="The capital city of Argentina is the Ciudad Autonoma de Buenos Aires (CABA)."
    )

    print(result)