"""
Medical Record Abstraction Environment Implementation.

Implements the OpenEnv Environment interface with step()/reset()/state().
Supports 3 tasks (easy → medium → hard) with deterministic grading.

Each episode:
  1. Agent calls reset() → receives initial observation
  2. Agent calls step(get_task) → receives task description
  3. Agent calls step(get_note) → receives clinical note
  4. Agent optionally calls step(get_drugs/get_guidelines) → reference data
  5. Agent calls step(submit, data=JSON) → receives graded score
"""

from __future__ import annotations

import random
from uuid import uuid4

from openenv.core.env_server.interfaces import Environment

try:
    from ..models import MedicalRecordAction, MedicalRecordObservation, MedicalRecordState
except ImportError:
    from models import MedicalRecordAction, MedicalRecordObservation, MedicalRecordState

try:
    from ..data.synthetic_notes import get_note, get_all_notes_for_task
    from ..data.drug_interactions import get_drug_database_text
except ImportError:
    from data.synthetic_notes import get_note, get_all_notes_for_task
    from data.drug_interactions import get_drug_database_text

try:
    from .graders import grade_submission
    from .reward import compute_reward
    from .tasks import (
        get_task_description,
        get_available_commands,
        get_max_steps,
        CLINICAL_GUIDELINES,
    )
except ImportError:
    from server.graders import grade_submission
    from server.reward import compute_reward
    from server.tasks import (
        get_task_description,
        get_available_commands,
        get_max_steps,
        CLINICAL_GUIDELINES,
    )


class MedicalRecordEnvironment(Environment):
    """
    Medical Record Abstraction Environment.

    A real-world clinical NLP environment where agents extract information
    from synthetic clinical notes with increasing difficulty:

    - Task 1 (Easy): Extract demographics, chief complaint, vital signs
    - Task 2 (Medium): Extract diagnoses + ICD-10, meds, detect drug conflicts
    - Task 3 (Hard): Risk assessment, critical flags, readmission scoring, summary

    Each task:
      - Has a set of available commands (action masking)
      - Has a maximum step limit
      - Is graded by a deterministic grader producing scores in [0.0, 1.0]

    Example:
        >>> env = MedicalRecordEnvironment()
        >>> obs = env.reset(task_id="task_1", note_id=0)
        >>> obs = env.step(MedicalRecordAction(command="get_task"))
        >>> obs = env.step(MedicalRecordAction(command="get_note"))
        >>> obs = env.step(MedicalRecordAction(command="submit", data='{"patient_name": "..."}'))
    """

    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self) -> None:
        """Initialize the environment with default state."""
        self._state = MedicalRecordState(episode_id=str(uuid4()), step_count=0)
        self._task_id: str = "task_1"
        self._note_id: int = 0
        self._note_data: dict = {}
        self._tools_called: list[str] = []
        self._submitted: bool = False
        self._current_score: float = 0.0
        self._max_steps: int = 5

    def reset(self, **kwargs) -> MedicalRecordObservation:
        """Reset the environment for a new episode.

        Keyword Args:
            task_id: "task_1", "task_2", or "task_3" (default: "task_1")
            note_id: Index of the clinical note (default: random)

        Returns:
            Initial observation with task context and available commands.
        """
        # Parse task_id and note_id from kwargs
        self._task_id = kwargs.get("task_id", "task_1")
        if self._task_id not in ("task_1", "task_2", "task_3"):
            self._task_id = "task_1"

        # Note selection
        all_notes = get_all_notes_for_task(self._task_id)
        if "note_id" in kwargs:
            self._note_id = int(kwargs["note_id"]) % len(all_notes)
        else:
            self._note_id = random.randint(0, len(all_notes) - 1)

        self._note_data = get_note(self._task_id, self._note_id)
        self._tools_called = []
        self._submitted = False
        self._current_score = 0.0
        self._max_steps = get_max_steps(self._task_id)

        # Reset internal state
        self._state = MedicalRecordState(
            episode_id=str(uuid4()),
            step_count=0,
            task_id=self._task_id,
            note_id=self._note_id,
            submitted=False,
            tools_called=[],
            current_score=0.0,
        )

        available = get_available_commands(self._task_id)

        return MedicalRecordObservation(
            done=False,
            reward=0.0,
            task_id=self._task_id,
            task_description="",
            clinical_note="",
            drug_database="",
            clinical_guidelines="",
            message=(
                f"Medical Record Abstraction Environment ready. "
                f"Task: {self._task_id} | Note: {self._note_id} | "
                f"Max steps: {self._max_steps}. "
                f"Use 'get_task' to see the task description."
            ),
            score_breakdown={},
            step_number=0,
            max_steps=self._max_steps,
            available_commands=available,
        )

    def step(self, action: MedicalRecordAction) -> MedicalRecordObservation:  # type: ignore[override]
        """Execute one step in the environment.

        Args:
            action: MedicalRecordAction with command and optional data.

        Returns:
            MedicalRecordObservation with results and feedback.
        """
        self._state.step_count += 1
        command = action.command.lower().strip()
        available = get_available_commands(self._task_id)

        # Check if episode is already done
        if self._submitted:
            return self._make_obs(
                done=True,
                reward=0.0,
                message="Episode already complete. Call reset() to start a new episode.",
            )

        # Check if over step limit
        if self._state.step_count > self._max_steps:
            reward = compute_reward(
                command, self._state.step_count, self._max_steps,
                available, self._tools_called,
            )
            return self._make_obs(
                done=True,
                reward=reward,
                message=(
                    f"Step limit exceeded ({self._state.step_count}/{self._max_steps}). "
                    f"Episode terminated with score 0.0."
                ),
            )

        # ──── COMMAND DISPATCH ────
        if command == "get_task":
            return self._handle_get_task(available)
        elif command == "get_note":
            return self._handle_get_note(available)
        elif command == "get_drugs":
            return self._handle_get_drugs(available)
        elif command == "get_guidelines":
            return self._handle_get_guidelines(available)
        elif command == "submit":
            return self._handle_submit(action.data, available)
        else:
            # Unknown command
            reward = compute_reward(
                command, self._state.step_count, self._max_steps,
                available, self._tools_called,
            )
            return self._make_obs(
                done=False,
                reward=reward,
                message=(
                    f"Unknown command '{command}'. "
                    f"Available commands: {', '.join(available)}"
                ),
            )

    @property
    def state(self) -> MedicalRecordState:
        """Get the current environment state."""
        self._state.task_id = self._task_id
        self._state.note_id = self._note_id
        self._state.submitted = self._submitted
        self._state.tools_called = list(self._tools_called)
        self._state.current_score = self._current_score
        return self._state

    # ──── COMMAND HANDLERS ────

    def _handle_get_task(self, available: list[str]) -> MedicalRecordObservation:
        """Return the task description and output schema."""
        reward = compute_reward(
            "get_task", self._state.step_count, self._max_steps,
            available, self._tools_called,
        )
        self._tools_called.append("get_task")

        return self._make_obs(
            done=False,
            reward=reward,
            task_description=get_task_description(self._task_id),
            message="Task description retrieved. Use 'get_note' to see the clinical note.",
        )

    def _handle_get_note(self, available: list[str]) -> MedicalRecordObservation:
        """Return the clinical note text."""
        reward = compute_reward(
            "get_note", self._state.step_count, self._max_steps,
            available, self._tools_called,
        )
        self._tools_called.append("get_note")

        note_text = self._note_data.get("text", "No note available.")

        extra_msg = ""
        if self._task_id in ("task_2", "task_3"):
            extra_msg = " Use 'get_drugs' to access the drug interaction database."
        if self._task_id == "task_3":
            extra_msg += " Use 'get_guidelines' for risk assessment guidelines."

        return self._make_obs(
            done=False,
            reward=reward,
            clinical_note=note_text,
            message=f"Clinical note retrieved.{extra_msg} Use 'submit' when ready.",
        )

    def _handle_get_drugs(self, available: list[str]) -> MedicalRecordObservation:
        """Return the drug interaction database."""
        if "get_drugs" not in available:
            reward = compute_reward(
                "get_drugs", self._state.step_count, self._max_steps,
                available, self._tools_called,
            )
            return self._make_obs(
                done=False,
                reward=reward,
                message="Drug database not available for this task.",
            )

        reward = compute_reward(
            "get_drugs", self._state.step_count, self._max_steps,
            available, self._tools_called,
        )
        self._tools_called.append("get_drugs")

        return self._make_obs(
            done=False,
            reward=reward,
            drug_database=get_drug_database_text(),
            message="Drug interaction database retrieved. Use 'submit' when ready.",
        )

    def _handle_get_guidelines(self, available: list[str]) -> MedicalRecordObservation:
        """Return clinical risk assessment guidelines (Task 3 only)."""
        if "get_guidelines" not in available:
            reward = compute_reward(
                "get_guidelines", self._state.step_count, self._max_steps,
                available, self._tools_called,
            )
            return self._make_obs(
                done=False,
                reward=reward,
                message="Clinical guidelines not available for this task.",
            )

        reward = compute_reward(
            "get_guidelines", self._state.step_count, self._max_steps,
            available, self._tools_called,
        )
        self._tools_called.append("get_guidelines")

        return self._make_obs(
            done=False,
            reward=reward,
            clinical_guidelines=CLINICAL_GUIDELINES,
            message="Clinical guidelines retrieved. Use 'submit' when ready.",
        )

    def _handle_submit(self, data: str, available: list[str]) -> MedicalRecordObservation:
        """Grade the agent's submission and end the episode."""
        ground_truth = self._note_data.get("ground_truth", {})

        score, breakdown = grade_submission(self._task_id, data, ground_truth)

        self._submitted = True
        self._current_score = score

        submission_score = score if "parse_error" not in breakdown else None
        reward = compute_reward(
            "submit", self._state.step_count, self._max_steps,
            available, self._tools_called,
            submission_score=submission_score,
        )
        self._tools_called.append("submit")

        # Build result message
        if "parse_error" in breakdown:
            message = (
                "SUBMISSION FAILED: Could not parse JSON. "
                "Please submit valid JSON matching the required output format. "
                "Score: 0.0"
            )
        else:
            message = (
                f"SUBMISSION GRADED. Score: {score:.4f}\n"
                f"Breakdown: {breakdown}\n"
                f"Steps used: {self._state.step_count}/{self._max_steps}"
            )

        return self._make_obs(
            done=True,
            reward=reward,
            message=message,
            score_breakdown=breakdown,
        )

    # ──── HELPER ────

    def _make_obs(
        self,
        done: bool,
        reward: float,
        message: str = "",
        task_description: str = "",
        clinical_note: str = "",
        drug_database: str = "",
        clinical_guidelines: str = "",
        score_breakdown: dict[str, float] | None = None,
    ) -> MedicalRecordObservation:
        """Construct an observation with current state."""
        available = get_available_commands(self._task_id)
        return MedicalRecordObservation(
            done=done,
            reward=reward,
            task_id=self._task_id,
            task_description=task_description,
            clinical_note=clinical_note,
            drug_database=drug_database,
            clinical_guidelines=clinical_guidelines,
            message=message,
            score_breakdown=score_breakdown or {},
            step_number=self._state.step_count,
            max_steps=self._max_steps,
            available_commands=available if not done else [],
            metadata={
                "note_id": self._note_id,
                "step": self._state.step_count,
                "submitted": self._submitted,
                "score": self._current_score,
            },
        )
