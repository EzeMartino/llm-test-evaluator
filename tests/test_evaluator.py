import pytest

from src.evaluator.llm_evaluator import evaluate, parse_response, validate_output


def test_evaluator_noLLM_exact_match():
    result = evaluate(
        prompt="What is the capital of France?",
        expected="Paris",
        actual="Paris",
        use_LLM=False
    )
    assert "label" in result
    assert "score" in result
    assert "explanation" in result
    assert result["label"] == "correct"
    assert result["score"] == 1.0
    
def test_evaluator_noLLM_partial_match():
    result = evaluate(
        prompt="What is the capital of France?",
        expected="Paris",
        actual="The capital of France is Paris",
        use_LLM=False
    )
    assert "label" in result
    assert "score" in result
    assert "explanation" in result
    assert result["label"] == "partially_correct"
    assert result["score"] == 0.7
    
def test_evaluator_noLLM_mismatch():
    result = evaluate(
        prompt="What is the capital of France?",
        expected="Paris",
        actual="Berlin",
        use_LLM=False
    )
    assert "label" in result
    assert "score" in result
    assert "explanation" in result
    assert result["label"] == "incorrect"
    assert result["score"] == 0
    
def test_validate_label():
    output = {
        "label": "almost_correct",
        "score": 0.6,
        "explanation": "Explanation"
    }
    with pytest.raises(ValueError, match="Invalid label"):
        validate_output(output)
        
def test_validate_score():
    output = {
        "label": "correct",
        "score": 3.9,
        "explanation": "Explanation"
    }
    with pytest.raises(ValueError, match="Invalid score"):
        validate_output(output)
        
def test_parse_response():
    raw_json_output = '{ "label": "correct", "score": 1, "explanation": "Explanation"}'
    parsed = parse_response(raw_json_output)
    
    assert isinstance(parsed, dict)

def test_parse_noisy_wrapper():
    raw_json_output = 'Sure, here goes the json: { "label": "correct", "score": 1, "explanation": "Explanation"}'
    parsed = parse_response(raw_json_output)
    assert isinstance(parsed, dict)