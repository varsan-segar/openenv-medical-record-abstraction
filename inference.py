#!/usr/bin/env python3
"""
Baseline Inference Script — Medical Record Abstraction Environment.

Uses the OpenAI chat completions API to run an agent against all 3 tasks.
Supports any OpenAI-compatible API via environment variables.

Environment Variables:
    API_BASE_URL      — API endpoint (default: https://api.openai.com/v1)
    MODEL_NAME        — Model to use (default: gpt-4o-mini)
    HF_TOKEN          — Authentication token (used as API key)

STDOUT FORMAT:
    [START] task=<task_name> env=<benchmark> model=<model_name>
    [STEP]  step=<n> action=<action_str> reward=<0.00> done=<true|false> error=<msg|null>
    [END]   success=<true|false> steps=<n> score=<score> rewards=<r1,r2,...,rn>

Usage:
    python inference.py
    API_BASE_URL=http://localhost:8000/v1 MODEL_NAME=my-model python inference.py
"""

import json
import os
import re
import sys

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
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY")

if not HF_TOKEN:
    print("WARNING: HF_TOKEN not set. LLM calls may fail.", file=sys.stderr, flush=True)

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
BENCHMARK = "medical_record_abstraction_env"


# ─── Structured Logging (START / STEP / END) — stdout only ───
def log_start(task: str, env_name: str, model: str) -> None:
    print(f"[START] task={task} env={env_name} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: str | None = None) -> None:
    error_val = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} "
        f"done={str(done).lower()} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: list) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} "
        f"score={score:.3f} rewards={rewards_str}",
        flush=True,
    )


# ─── Debug helper (stderr only, never stdout) ───
def debug(msg: str) -> None:
    print(f"[DEBUG] {msg}", file=sys.stderr, flush=True)


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


def _parse_action(text: str) -> MedicalRecordAction | None:
    """Parse an action from LLM text output."""
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


def run_episode(task_id: str, note_id: int) -> dict:
    """Run a single episode and return results."""
    env = MedicalRecordEnvironment()
    rewards: list[float] = []
    steps = 0
    final_score = 0.0
    success = False

    log_start(task_id, BENCHMARK, MODEL_NAME)

    try:
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
                debug(f"API error: {e}")
                log_step(steps + 1, "error", 0.0, False, str(e))
                break

            messages.append({"role": "assistant", "content": assistant_msg})

            # Parse action from LLM response
            action = _parse_action(assistant_msg)
            if action is None:
                messages.append({"role": "user", "content": (
                    "I couldn't parse your action. Please respond with exactly:\n"
                    '{"command": "<command_name>", "data": "<for_submit_only>"}'
                )})
                steps += 1
                continue

            # Step the environment
            obs = env.step(action)
            reward = obs.reward
            rewards.append(reward)
            steps += 1

            # Structured logging — immediately after env.step()
            log_step(steps, action.command, reward, obs.done)

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
                final_score = env.state.current_score
                # Clamp to strictly (0, 1) — validator rejects 0.0 and 1.0
                final_score = max(0.001, min(0.999, final_score))
                success = final_score > 0.001

            messages.append({"role": "user", "content": obs_text})

    finally:
        # [END] is ALWAYS emitted, even on exception
        log_end(success=success, steps=steps, score=final_score, rewards=rewards)

    return {
        "task_id": task_id,
        "note_id": note_id,
        "steps": steps,
        "total_reward": round(sum(rewards), 4),
        "final_score": round(final_score, 4),
        "score_breakdown": dict(obs.score_breakdown) if obs.done else {},
    }


def main():
    """Run baseline inference across all tasks."""
    debug(f"API: {API_BASE_URL} | Model: {MODEL_NAME}")

    all_results = []
    notes_per_task = 2

    for task_id in ["task_1", "task_2", "task_3"]:
        debug(f"Running {task_id}...")

        for note_id in range(notes_per_task):
            try:
                result = run_episode(task_id, note_id)
                all_results.append(result)
                debug(f"  {task_id}/note_{note_id}: score={result['final_score']:.4f}")
            except Exception as e:
                debug(f"  {task_id}/note_{note_id}: ERROR: {e}")
                all_results.append({
                    "task_id": task_id, "note_id": note_id,
                    "error": str(e), "final_score": 0.0,
                })

    # Save results to file (no stdout output)
    outputs_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    results_path = os.path.join(outputs_dir, "inference_results.json")
    with open(results_path, "w") as f:
        json.dump({"results": all_results}, f, indent=2)
    debug(f"Results saved to {results_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[END] success=false steps=0 score=0.000 rewards=0.00", flush=True)
        debug(f"FATAL: {exc}")
        sys.exit(1)
