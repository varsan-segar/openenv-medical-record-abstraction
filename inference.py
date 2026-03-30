#!/usr/bin/env python3
"""
Baseline Inference Script — Medical Record Abstraction Environment.

Uses the OpenAI chat completions API to run an agent against all 3 tasks.
Supports any OpenAI-compatible API via environment variables.

Environment Variables:
    API_BASE_URL  — API endpoint (default: https://api.openai.com/v1)
    MODEL_NAME    — Model to use (default: gpt-4o-mini)
    HF_TOKEN      — Authentication token (used as API key)

Usage:
    python inference.py
    API_BASE_URL=http://localhost:8000/v1 MODEL_NAME=my-model python inference.py
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openai import OpenAI
from server.environment import MedicalRecordEnvironment
from models import MedicalRecordAction

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ─── Configuration ───
API_BASE_URL = os.environ.get("API_BASE_URL")
MODEL_NAME = os.environ.get("MODEL_NAME")
# Use HF_TOKEN as primary, OPENAI_API_KEY as fallback just in case
HF_TOKEN = os.environ.get("HF_TOKEN") or os.environ.get("OPENAI_API_KEY")

if not all([API_BASE_URL, MODEL_NAME, HF_TOKEN]):
    print("ERROR: Missing required environment variables.", file=sys.stderr)
    print("Please ensure API_BASE_URL, MODEL_NAME, and HF_TOKEN are set.", file=sys.stderr)
    print("Example: API_BASE_URL='https://api.openai.com/v1' MODEL_NAME='gpt-4o-mini' HF_TOKEN='your_token'", file=sys.stderr)
    sys.exit(1)

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
env = MedicalRecordEnvironment()

# ─── System prompt ───
SYSTEM_PROMPT = """\
You are a medical record abstraction assistant. You interact with an environment
using commands to extract clinical information from patient notes.

IMPORTANT RULES:
1. Always start with 'get_task' to understand what to extract.
2. Then use 'get_note' to read the clinical note.
3. For Task 2+, use 'get_drugs' to check drug interactions.
4. For Task 3, also use 'get_guidelines' for risk assessment criteria.
5. Finally, use 'submit' with your extraction as valid JSON.

When you decide on an action, respond with EXACTLY this JSON format:
{"command": "<command_name>", "data": "<json_string_for_submit_only>"}

For submit, the 'data' field must contain the JSON extraction as a STRING.
For other commands, leave 'data' empty or omit it.
"""


def run_episode(task_id: str, note_id: int) -> dict:
    """Run a single episode and return results."""
    obs = env.reset(task_id=task_id, note_id=note_id)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": (
            f"Task: {task_id} | Note: {note_id}\n"
            f"Available commands: {obs.available_commands}\n"
            f"Max steps: {obs.max_steps}\n"
            f"{obs.message}\n\n"
            "Start by getting the task description."
        )},
    ]

    total_reward = 0.0
    final_score = 0.0
    steps = 0

    while not obs.done and steps < obs.max_steps + 2:
        # Call the LLM
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.0,
                max_tokens=2000,
            )
            assistant_msg = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"  API error: {e}")
            break

        messages.append({"role": "assistant", "content": assistant_msg})

        # Parse action from LLM response
        action = _parse_action(assistant_msg)
        if action is None:
            # Try to extract JSON from the response
            messages.append({"role": "user", "content": (
                "I couldn't parse your action. Please respond with exactly:\n"
                '{"command": "<command_name>", "data": "<for_submit_only>"}'
            )})
            steps += 1
            continue

        # Step the environment
        obs = env.step(action)
        total_reward += obs.reward
        steps += 1

        # Build user message with observation
        obs_text = f"Step {obs.step_number}/{obs.max_steps} | Reward: {obs.reward:.4f}\n"
        if obs.task_description:
            obs_text += f"\nTask Description:\n{obs.task_description}\n"
        if obs.clinical_note:
            obs_text += f"\nClinical Note:\n{obs.clinical_note}\n"
        if obs.drug_database:
            obs_text += f"\nDrug Database:\n{obs.drug_database[:2000]}\n"
        if obs.clinical_guidelines:
            obs_text += f"\nClinical Guidelines:\n{obs.clinical_guidelines}\n"
        if obs.message:
            obs_text += f"\nMessage: {obs.message}\n"
        if obs.done:
            obs_text += "\n[EPISODE COMPLETE]"
            final_score = obs.score_breakdown.get("total", obs.reward)
            # Try to get the actual grader score from state
            final_score = env.state.current_score

        messages.append({"role": "user", "content": obs_text})

    return {
        "task_id": task_id,
        "note_id": note_id,
        "steps": steps,
        "total_reward": round(total_reward, 4),
        "final_score": round(final_score, 4),
        "score_breakdown": dict(obs.score_breakdown) if obs.done else {},
    }


def _parse_action(text: str) -> MedicalRecordAction | None:
    """Parse an action from LLM text output."""
    # Try to find JSON in the response
    text = text.strip()

    # Try direct parse
    try:
        data = json.loads(text)
        if "command" in data:
            return MedicalRecordAction(
                command=data["command"],
                data=data.get("data", ""),
            )
    except (json.JSONDecodeError, ValueError):
        pass

    # Try to find JSON block in markdown
    import re
    json_blocks = re.findall(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    for block in json_blocks:
        try:
            data = json.loads(block.strip())
            if "command" in data:
                return MedicalRecordAction(
                    command=data["command"],
                    data=data.get("data", ""),
                )
        except (json.JSONDecodeError, ValueError):
            continue

    # Try to find JSON object anywhere in text
    json_match = re.search(r'\{[^{}]*"command"[^{}]*\}', text)
    if json_match:
        try:
            data = json.loads(json_match.group())
            return MedicalRecordAction(
                command=data["command"],
                data=data.get("data", ""),
            )
        except (json.JSONDecodeError, ValueError):
            pass

    return None


def main():
    """Run baseline inference across all tasks."""
    print("=" * 70)
    print("Medical Record Abstraction — Baseline Inference")
    print(f"API: {API_BASE_URL} | Model: {MODEL_NAME}")
    print("=" * 70)

    all_results = []
    task_scores = {"task_1": [], "task_2": [], "task_3": []}

    # Run 2 notes per task for baseline (8 total would take too long)
    notes_per_task = 2

    for task_id in ["task_1", "task_2", "task_3"]:
        print(f"\n{'─' * 50}")
        print(f"Running {task_id}...")
        print(f"{'─' * 50}")

        for note_id in range(notes_per_task):
            print(f"\n  Note {note_id}:", end=" ")
            start = time.time()

            try:
                result = run_episode(task_id, note_id)
                elapsed = time.time() - start
                result["time_seconds"] = round(elapsed, 1)

                print(f"score={result['final_score']:.4f}, "
                      f"steps={result['steps']}, "
                      f"time={elapsed:.1f}s")

                all_results.append(result)
                task_scores[task_id].append(result["final_score"])
            except Exception as e:
                print(f"ERROR: {e}")
                all_results.append({
                    "task_id": task_id, "note_id": note_id,
                    "error": str(e), "final_score": 0.0,
                })
                task_scores[task_id].append(0.0)

    # Summary
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)

    for task_id, scores in task_scores.items():
        avg = sum(scores) / len(scores) if scores else 0.0
        print(f"  {task_id}: avg={avg:.4f} | scores={scores}")

    overall = sum(s for scores in task_scores.values() for s in scores)
    total_n = sum(len(s) for s in task_scores.values())
    print(f"\n  Overall average: {overall / total_n:.4f}" if total_n else "")

    # Save results into the standard openenv outputs directory
    outputs_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    results_path = os.path.join(outputs_dir, "inference_results.json")
    with open(results_path, "w") as f:
        json.dump({
            "config": {
                "api_base_url": API_BASE_URL,
                "model_name": MODEL_NAME,
                "notes_per_task": notes_per_task,
            },
            "task_scores": {k: {"mean": sum(v)/len(v) if v else 0, "scores": v}
                           for k, v in task_scores.items()},
            "results": all_results,
        }, f, indent=2)
    print(f"\nResults saved to {results_path}")


if __name__ == "__main__":
    main()
