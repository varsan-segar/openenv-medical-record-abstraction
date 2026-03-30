"""
Reward Shaping — Medical Record Abstraction Environment.

Provides continuous reward signal across the episode trajectory.
Designed to encourage:
  - Information gathering (exploring available tools)
  - Efficient task completion (not wasting steps)
  - Quality submissions (grader score as primary signal)

Penalizes:
  - Redundant tool calls
  - Invalid commands
  - Step overshoot beyond max_steps
  - Malformed submissions
"""

from __future__ import annotations


def compute_reward(
    command: str,
    step_count: int,
    max_steps: int,
    available_commands: list[str],
    tools_called: list[str],
    submission_score: float | None = None,
) -> float:
    """Compute the reward for a single step.

    Args:
        command: The command the agent executed.
        step_count: Current step number (1-indexed).
        max_steps: Maximum allowed steps for this task.
        available_commands: Commands available for this task.
        tools_called: Commands already called (before this step).
        submission_score: If command is 'submit', the grader score (0.0–1.0).
                         None if submission failed to parse.

    Returns:
        Reward value, clamped to [-1.0, 1.0].
    """
    reward = 0.0

    # ① Info-gathering reward: +0.02 for first use of a tool
    info_commands = {"get_note", "get_task", "get_drugs", "get_guidelines"}
    if command in info_commands:
        if command not in tools_called:
            reward += 0.02  # First call — useful exploration
        else:
            reward -= 0.05  # Redundant call — penalize waste

    # ② Submission: the grader score is the primary reward signal
    if command == "submit":
        if submission_score is not None:
            reward += submission_score
        else:
            reward -= 0.3  # Failed to parse JSON — significant penalty

    # ③ Invalid command penalty
    if command not in available_commands:
        reward -= 0.1

    # ④ Step overshoot penalty (applied per step over max)
    if step_count > max_steps:
        reward -= 0.1

    # Clamp to [-1.0, 1.0]
    return max(-1.0, min(1.0, reward))
