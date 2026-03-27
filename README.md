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
### Run tests
```bash
pytest
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

## API Contract

### Input

The evaluator expects the following fields:

- `prompt` (string): The original instruction given to the model
- `expected` (string): The reference or expected answer
- `actual` (string): The model-generated answer to evaluate

### Output

The evaluator returns:

- `label` (string): One of `correct`, `partially_correct`, `incorrect`
- `score` (float): A value between 0 and 1 indicating answer quality
- `explanation` (string): Short explanation of the evaluation

### Example
#### Input
```json
{
  "prompt": "What is the most populated country in 2026?",
  "expected": "India",
  "actual": "The most populated country in 2026 is India."
}
```
#### Output
```json
{
  "label": "correct",
  "score": 1.0,
  "explanation": "The actual answer matches the expected answer."
}
```


## Evaluation Modes

The evaluator supports two modes:

- **LLM mode**: uses an OpenAI model for semantic evaluation
- **Rule-based mode**: deterministic fallback for reliability and testing

If the LLM is unavailable or disabled, the evaluator automatically falls back to the rule-based mode.


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