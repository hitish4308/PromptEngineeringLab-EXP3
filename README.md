# Prompt Engineering Lab - Experiment 3

## Iterative Prompt Refinement

Demonstrates how successive refinements to a prompt improve output
quality for a specific audience and goal.

## Task

Explain photosynthesis to a 10-year-old.

## Refinement Path

| Iteration | What Changed | Purpose |
|-----------|--------------|---------|
| 0 - Baseline | "Explain photosynthesis to a 10-year-old." | Raw output for comparison |
| 1 - Refine | Added role, analogy, sentence limit, jargon ban | Child-friendly tone |
| 2 - Refine | Added mnemonic and diagram description | Retention and visualization |

## Model and Parameters

- Model: openai/gpt-oss-20b
- Temperature: 0.5 (fixed for fair comparison)
- Max tokens: 800

## Setup

Reuse the environment from Experiment 1:

    Copy-Item ..\EXP_1\.env .
    python -m pip install -r requirements.txt

## Run

    python refine_prompts.py

## Expected Output

Three iteration blocks, each with:

- The prompt sent
- The model response
- An analysis comment
- Character and word counts

Followed by a final summary comparing all iterations.

## Key Findings

- The baseline response is accurate but verbose and uses markdown tables
  and headers - not ideal for a 10-year-old
- Adding role + analogy + length constraint tightens the response
  dramatically (char count drops)
- Adding a mnemonic + diagram hint adds memory aids without bloating
  the answer

## Constraints

- Same model and parameters across all iterations
- Only the prompt changes
- Task remains unchanged throughout

## Security

- Never commit .env
- Never paste API keys in chat, logs, or screenshots

## License

For educational / lab use only.
