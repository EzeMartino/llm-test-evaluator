import pytest

from src.evaluator.llm_evaluator import evaluate, parse_response, validate_output
from src.schemas import EvaluationLabel, EvaluationResponse


def test_evaluator_no_llm_exact_match():
    result = evaluate(
        prompt="What is the capital of France?",
        expected="Paris",
        actual="Paris",
        use_LLM=False,
    )

    assert isinstance(result, EvaluationResponse)
    assert result.label == EvaluationLabel.correct
    assert result.score == 1.0
    assert result.explanation == "Exact match"


def test_evaluator_no_llm_partial_match():
    result = evaluate(
        prompt="What is the capital of France?",
        expected="Paris",
        actual="The capital of France is Paris",
        use_LLM=False,
    )

    assert isinstance(result, EvaluationResponse)
    assert result.label == EvaluationLabel.partially_correct
    assert result.score == 0.7
    assert result.explanation == "Expected answer is contained in actual answer"


def test_evaluator_no_llm_mismatch():
    result = evaluate(
        prompt="What is the capital of France?",
        expected="Paris",
        actual="Berlin",
        use_LLM=False,
    )

    assert isinstance(result, EvaluationResponse)
    assert result.label == EvaluationLabel.incorrect
    assert result.score == 0.0
    assert result.explanation == "Answer does not match expected"


def test_validate_output_accepts_valid_payload():
    output = {
        "label": "correct",
        "score": 1.0,
        "explanation": "Explanation",
    }

    validated = validate_output(output)

    assert isinstance(validated, EvaluationResponse)
    assert validated.label == EvaluationLabel.correct
    assert validated.score == 1.0
    assert validated.explanation == "Explanation"


def test_validate_output_rejects_invalid_label():
    output = {
        "label": "almost_correct",
        "score": 0.6,
        "explanation": "Explanation",
    }

    with pytest.raises(ValueError, match="Invalid evaluator output"):
        validate_output(output)


def test_validate_output_rejects_invalid_score():
    output = {
        "label": "correct",
        "score": 3.9,
        "explanation": "Explanation",
    }

    with pytest.raises(ValueError, match="Invalid evaluator output"):
        validate_output(output)


def test_parse_response():
    raw_json_output = '{"label": "correct", "score": 1, "explanation": "Explanation"}'
    parsed = parse_response(raw_json_output)

    assert isinstance(parsed, dict)
    assert parsed["label"] == "correct"
    assert parsed["score"] == 1
    assert parsed["explanation"] == "Explanation"


def test_parse_noisy_wrapper():
    raw_json_output = 'Sure, here goes the json: {"label": "correct", "score": 1, "explanation": "Explanation"}'
    parsed = parse_response(raw_json_output)

    assert isinstance(parsed, dict)
    assert parsed["label"] == "correct"
    assert parsed["score"] == 1
    assert parsed["explanation"] == "Explanation"