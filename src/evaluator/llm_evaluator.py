# from openai import OpenAI
import json
import re
from src.evaluator.providers import call_openai
from src.evaluator.rule_based import rule_based_evaluate
from src.config import USE_LLM

SYSTEM_PROMPT = """
    You are an evaluator for LLM-generated answers.

    Your task is to compare an actual answer against an expected answer given a prompt.

    You must classify the answer as one of:
    - correct
    - partially_correct
    - incorrect

    Definitions:
    - correct: The answer matches the expected answer in all essential information.
    - partially_correct: The answer is incomplete or contains minor inaccuracies.
    - incorrect: The answer is wrong or contradicts the expected answer.

    You must return a JSON object with:
    - label: one of ["correct", "partially_correct", "incorrect"]
    - score: a float between 0 and 1
    - explanation: a short explanation

    Return ONLY valid JSON. No extra text.
    """
    
VALID_LABELS = {"correct", "partially_correct", "incorrect"}

def call_llm_mock(system_prompt, user_prompt):
    if "Paris" not in user_prompt:
        return """
        {
            "label": "incorrect",
            "score": 0.0,
            "explanation": "Wrong capital"
        }
        """
    return """
    {
        "label": "correct",
        "score": 1.0,
        "explanation": "Mock response"
    }
    """

def build_prompt(prompt, expected, actual):
    return f"""
        Prompt:
        {prompt}

        Expected Answer:
        {expected}

        Actual Answer:
        {actual}
    """
    
def parse_response(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Invalid JSON response: {text}")
    
def validate_output(output):
    if "label" not in output or "score" not in output or "explanation" not in output:
        raise ValueError("Missing required fields")
    
    if output["label"] not in VALID_LABELS:
        raise ValueError("Invalid label")
    
    if not isinstance(output["score"], (int, float)):
        raise ValueError("Score must be numeric")

    if not (0 <= output["score"] <= 1):
        raise ValueError("Invalid score")
    
    if not isinstance(output["explanation"], str):
        raise ValueError("Explanation must be string")
    
    return output

def evaluate(prompt: str, expected: str, actual: str) -> dict:
    if not USE_LLM:
        return rule_based_evaluate(expected, actual)
    user_prompt = build_prompt(prompt, expected, actual)
    try:
        raw_output = call_openai(SYSTEM_PROMPT, user_prompt)
        parsed = parse_response(raw_output)
        validated_output = validate_output(parsed)
        return validated_output
    except Exception as e:
        # Automatic fallback if LLM fails
        fallback = rule_based_evaluate(expected, actual)
        fallback["explanation"] += f" (Fallback used because the LLM evaluator was unavailable)"
        return fallback

if __name__ == "__main__":
    result = evaluate(
        prompt="What is the capital of Argentina?",
        expected="Buenos Aires",
        actual="The capital city of Argentina is the Ciudad Autonoma de Buenos Aires (CABA)."
    )

    print(result)