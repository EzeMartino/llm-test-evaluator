from src.schemas import EvaluationResponse, EvaluationLabel


def rule_based_evaluate(expected: str, actual: str) -> dict:
    expected_clean = expected.strip().lower()
    actual_clean = actual.strip().lower()

    if expected_clean == actual_clean:
        return EvaluationResponse(
            label= EvaluationLabel.correct,
            score= 1.0,
            explanation= "Exact match"
        )

    if expected_clean in actual_clean:
        return EvaluationResponse(
            label= EvaluationLabel.partially_correct,
            score= 0.7,
            explanation= "Expected answer is contained in actual answer"
        )

    return EvaluationResponse(
            label= EvaluationLabel.incorrect,
            score= 0,
            explanation= "Answer does not match expected"
        )
