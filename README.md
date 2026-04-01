# LLM Test Evaluator


## Problem
Evaluating LLM outputs is non-trivial, especially when correctness is subjective or partially correct.
In many real-world scenarios (e.g. QA, testing, or content validation), we need a consistent way to compare a generated response against an expected one.
This project provides a simple LLM-based evaluator that scores and classifies responses in a structured and reproducible way.


## Scope (V1)

This project evaluates whether an LLM-generated answer matches an expected answer.

Version 1 is intentionally limited to text-based evaluation using three inputs:

- prompt
- expected answer
- actual answer

The evaluator returns:
- a label (`correct`, `partially_correct`, or `incorrect`)
- a numeric score between 0 and 1
- a short explanation

Out of scope for V1:
- retrieval-augmented generation (RAG)
- external knowledge verification
- image or multimodal evaluation
- long multi-turn conversations
- production-scale monitoring


## Project Structure
```text
data/          raw and processed data
src/           source code
src/evaluator  evaluator logic handler
src/api        endpoints handler
tests/         automated tests
```

## Evaluation Modes
The evaluator supports two modes:
- **LLM mode**: uses an OpenAI model for semantic evaluation
- **Rule-based mode**: deterministic fallback for reliability and testing

If the LLM is unavailable or disabled, the evaluator automatically falls back to the rule-based mode.


## API Contract
### GET /health
#### Response
```json
{
  "status": "ok"
}
```

### POST /evaluate
#### Request body
```json
{
  "prompt": "What is the most populated country in 2026?",
  "expected": "India",
  "actual": "The most populated country in 2026 is India."
}
```
##### Response
```json
{
  "label": "correct",
  "score": 1.0,
  "explanation": "The actual answer matches the expected answer."
}
```
##### Error responses
The API may return the following error codes:
- `400 Bad Request`: controlled evaluation error (for example, invalid evaluator output)
- `422 Unprocessable Entity`: invalid request payload
- `500 Internal Server Error`: unexpected internal failure


## Evaluation Response
The evaluator always returns a structured response with:
- `label`: one of `correct`, `partially_correct`, or `incorrect`
- `score`: a float between `0.0` and `1.0`
- `explanation`: a short human-readable explanation of the decision

Label meaning:
- `correct`: the actual answer matches the expected answer in all essential information
- `partially_correct`: the answer is incomplete, broader than expected, or contains minor inaccuracies
- `incorrect`: the answer is wrong or misses the expected meaning


## How to run
```bash
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```
Then open:
http://localhost:8000/docs


## Setup
### Clone Repo
### Create virtual environment
Windows:
```bash
python -m venv .venv
source .venv\\Scripts\\activate
```
Linux/Mac:
```bash
source .venv/bin/activate
```
### Install dependencies
```bash
pip install -r requirements.txt
```
### Run API:
```bash
uvicorn src.api.main:app --reload
```
### Set OpenAI API key
Windows PowerShell:
```bash
$env:OPENAI_API_KEY="your_api_key"
```
Linux/Mac:
```bash
export OPENAI_API_KEY="your_api_key"
```


## Testing
Run all tests:
```bash
pytest -q
```
Tests cover:
- evaluator logic (rule-based + validation)
- JSON parsing robustness
- API contract
- HTTP error handling


## Use cases
- Evaluating LLM responses in automated testing pipelines
- Validating AI-generated content against expected outputs
- Assisting QA processes for AI-powered systems
- Benchmarking prompt or model performance


## Current Status
Version 1 supports:
- structured evaluation via API
- LLM-based scoring
- deterministic fallback mode
- input validation with FastAPI/Pydantic