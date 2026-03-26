# from openai import OpenAI
import json
# client = OpenAI()

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

# def call_llm_API(system_prompt, user_prompt):
#    response = client.chat.completions.create(
#        model="gpt-4o-mini",
#        temperature=0,
#        messages=[
#            {"role": "system", "content": system_prompt},
#            {"role": "user", "content": user_prompt},
#        ],
#    )
#    return response.choices[0].message.content

def call_llm_mock(system_prompt, user_prompt):
    if "Berlin" in user_prompt:
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
    
def parse_response(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON response: {text}")
    
def validate_output(output):
    if output["label"] not in VALID_LABELS:
        raise ValueError("Invalid label")

    if not (0 <= output["score"] <= 1):
        raise ValueError("Invalid score")
    return output

def evaluate(prompt: str, expected: str, actual: str) -> dict:
    user_prompt = build_prompt(prompt, expected, actual)
    raw_output = call_llm_mock(SYSTEM_PROMPT, user_prompt)
    parsed = parse_response(raw_output)
    validated_output = validate_output(parsed)
    return validated_output

if __name__ == "__main__":
    result = evaluate(
        prompt="What is the capital of France?",
        expected="Paris",
        actual="The capital of France is Paris."
    )

    print(result)