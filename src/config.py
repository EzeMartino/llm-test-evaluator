USE_LLM = True # Change to false for fallback rule-based

MODEL_NAME = "gpt-5.4-nano"

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