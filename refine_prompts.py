"""
Experiment 3 - Iterative Prompt Refinement

Task: Explain photosynthesis to a 10-year-old.
Starts with a baseline prompt, then applies two refinements:
  Round 1 - Add role, analogy, length constraint, jargon ban
  Round 2 - Add mnemonic, diagram description
"""

import os
import textwrap
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# ---------- Setup ----------
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.environ.get("NVIDIA_API_KEY")
if not api_key:
    raise SystemExit("NVIDIA_API_KEY not found. Create a .env file.")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key,
)

MODEL = "openai/gpt-oss-20b"
TEMPERATURE = 0.5
MAX_TOKENS = 800


# ---------- Helper ----------
def ask_llm(prompt: str) -> str:
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            stream=False,
        )
        content = resp.choices[0].message.content
        return (content or "").strip() or "[no content returned]"
    except Exception as e:
        return f"[API error] {type(e).__name__}: {e}"


def show_iteration(index: int, label: str, prompt: str, response: str, analysis: str):
    width = 72
    print("=" * width)
    print(f"  ITERATION {index} - {label}")
    print("=" * width)
    print("PROMPT:")
    print(textwrap.indent(prompt, "  "))
    print()
    print("RESPONSE:")
    print(textwrap.indent(response, "  "))
    print()
    print("ANALYSIS:")
    print(textwrap.indent(analysis, "  "))
    print()
    print(f"  [chars: {len(response)} | words: {len(response.split())}]")
    print()


# ---------- Prompts ----------
ITERATIONS = [
    {
        "label": "BASELINE",
        "prompt": "Explain photosynthesis to a 10-year-old.",
        "analysis": (
            "Baseline output may be accurate but can include technical jargon "
            "and lacks a child-friendly structure. Likely too formal."
        ),
    },
    {
        "label": "ADD ROLE + ANALOGY + LENGTH",
        "prompt": (
            "You are a friendly science teacher. "
            "Explain photosynthesis to a 10-year-old using a simple analogy "
            "(like a kitchen or factory). "
            "Keep the explanation to 3 short sentences and avoid technical jargon."
        ),
        "analysis": (
            "Adding a role, an analogy, and a sentence limit shifts the response "
            "from textbook prose toward conversational, memorable teaching. "
            "The jargon ban removes words like 'chlorophyll' or 'glucose'."
        ),
    },
    {
        "label": "ADD MNEMONIC + DIAGRAM HINT",
        "prompt": (
            "You are a friendly science teacher. "
            "Explain photosynthesis to a 10-year-old using a simple analogy. "
            "Keep it to 3 short sentences, avoid technical jargon, "
            "include a memory trick for the word 'photosynthesis', "
            "and describe what a simple drawing of the process would show."
        ),
        "analysis": (
            "Adding a mnemonic aids recall; the diagram description adds a "
            "visual dimension. This refines engagement and retention, the two "
            "goals most relevant for a 10-year-old audience."
        ),
    },
]


# ---------- Main ----------
if __name__ == "__main__":
    print(f"Model: {MODEL}")
    print(f"Temperature: {TEMPERATURE} | Max tokens: {MAX_TOKENS}")
    print()

    for i, item in enumerate(ITERATIONS):
        response = ask_llm(item["prompt"])
        show_iteration(i, item["label"], item["prompt"], response, item["analysis"])

    print("=" * 72)
    print("  FINAL SUMMARY")
    print("=" * 72)
    print("""
- Iteration 0 (baseline) provided a technically accurate explanation
  but was not tailored to a 10-year-old audience.

- Iteration 1 (role + analogy + length limit + jargon ban) transformed
  the explanation into a conversational teaching moment.

- Iteration 2 (mnemonic + diagram) added two memory aids.

Result: Each refinement addressed a specific weakness in the prior
output. Iterative prompting is a structured way to steer an LLM toward
the target quality without changing the underlying task.
""")
