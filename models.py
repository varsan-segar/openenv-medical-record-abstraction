# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Data models for the Medical Record Abstraction Environment.

Defines the typed Pydantic models for Action, Observation, and State
that form the API contract between agent and environment.

Action Space:
    command: one of "get_task", "get_note", "get_drugs", "get_guidelines", "submit"
    data: JSON string payload (used only for "submit" command)

Observation Space:
    Inherits done/reward from Observation base.
    Provides clinical_note, task_description, drug_database, clinical_guidelines,
    score_breakdown, and agent guidance (available_commands, message).

State Space:
    Inherits episode_id/step_count from State base.
    Tracks task_id, note_id, submission status, tools called, and current score.
"""

from typing import Dict, List, Optional

from openenv.core.env_server.types import Action, Observation, State
from pydantic import Field


# ─── ACTION ────────────────────────────────────────────────────

class MedicalRecordAction(Action):
    """Agent's action: what command to execute and with what data.

    Commands:
        get_task       — Retrieve the task description and output schema.
        get_note       — Retrieve the clinical note text.
        get_drugs      — Retrieve the drug interaction database (Task 2+).
        get_guidelines — Retrieve clinical risk guidelines (Task 3 only).
        submit         — Submit extraction as JSON string in `data` field.
    """

    command: str = Field(
        ...,
        description=(
            "Command to execute. One of: "
            "'get_task', 'get_note', 'get_drugs', 'get_guidelines', 'submit'"
        ),
    )
    data: str = Field(
        default="",
        description="JSON string payload for the 'submit' command. Empty for other commands.",
    )


# ─── OBSERVATION ───────────────────────────────────────────────

class MedicalRecordObservation(Observation):
    """What the agent sees after each action.

    Inherits from Observation base:
        done: bool      — Whether the episode has terminated.
        reward: float   — Reward signal from the last action.
        metadata: dict  — Additional metadata.
    """

    # Task context
    task_id: str = Field(
        default="",
        description="Current task identifier (task_1, task_2, or task_3).",
    )
    task_description: str = Field(
        default="",
        description="Human-readable description of what to extract and the output JSON schema.",
    )

    # Clinical data (populated by get_note, get_drugs, get_guidelines)
    clinical_note: str = Field(
        default="",
        description="The raw clinical note text to process.",
    )
    drug_database: str = Field(
        default="",
        description="Drug interaction reference data (available in Task 2 and 3).",
    )
    clinical_guidelines: str = Field(
        default="",
        description="Clinical risk assessment guidelines (available in Task 3 only).",
    )

    # Feedback
    message: str = Field(
        default="",
        description="Feedback message from the environment (status updates, errors, results).",
    )
    score_breakdown: Dict[str, float] = Field(
        default_factory=dict,
        description="Detailed grading breakdown on submission (component → score).",
    )

    # Step tracking
    step_number: int = Field(
        default=0,
        description="Current step number in the episode.",
    )
    max_steps: int = Field(
        default=10,
        description="Maximum allowed steps for this task.",
    )

    # Dynamic action masking
    available_commands: List[str] = Field(
        default_factory=list,
        description="Commands available to the agent at this step.",
    )


# ─── STATE ─────────────────────────────────────────────────────

class MedicalRecordState(State):
    """Internal environment state exposed via the state() endpoint.

    Inherits from State base:
        episode_id: Optional[str] — Unique episode identifier.
        step_count: int           — Number of steps taken.
    """

    task_id: str = Field(
        default="",
        description="Current task being performed.",
    )
    note_id: int = Field(
        default=0,
        description="Index of the clinical note within the task's note bank.",
    )
    submitted: bool = Field(
        default=False,
        description="Whether the agent has submitted an answer.",
    )
    tools_called: List[str] = Field(
        default_factory=list,
        description="List of commands the agent has called so far.",
    )
    current_score: float = Field(
        default=0.0,
        description="Score from the most recent submission (0.0 if not yet submitted).",
    )
