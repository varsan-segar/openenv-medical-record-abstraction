# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""Medical Record Abstraction Environment Client."""

from typing import Dict

from openenv.core import EnvClient
from openenv.core.client_types import StepResult

from .models import MedicalRecordAction, MedicalRecordObservation, MedicalRecordState


class MedicalRecordEnv(
    EnvClient[MedicalRecordAction, MedicalRecordObservation, MedicalRecordState]
):
    """
    Client for the Medical Record Abstraction Environment.

    Maintains a persistent WebSocket connection to the environment server.
    Each client instance has its own dedicated environment session.

    Example:
        >>> with MedicalRecordEnv(base_url="http://localhost:8000") as client:
        ...     result = client.reset()
        ...     print(result.observation.message)
        ...
        ...     result = client.step(MedicalRecordAction(command="get_task"))
        ...     print(result.observation.task_description)
        ...
        ...     result = client.step(MedicalRecordAction(command="get_note"))
        ...     print(result.observation.clinical_note)
        ...
        ...     result = client.step(MedicalRecordAction(command="submit", data='{"key": "val"}'))
        ...     print(result.observation.score_breakdown)
    """

    def _step_payload(self, action: MedicalRecordAction) -> Dict:
        """Convert action to JSON payload for step message."""
        payload = {"command": action.command}
        if action.data:
            payload["data"] = action.data
        return payload

    def _parse_result(self, payload: Dict) -> StepResult[MedicalRecordObservation]:
        """Parse server response into StepResult."""
        obs_data = payload.get("observation", {})
        observation = MedicalRecordObservation(
            done=payload.get("done", False),
            reward=payload.get("reward", 0.0),
            task_id=obs_data.get("task_id", ""),
            task_description=obs_data.get("task_description", ""),
            clinical_note=obs_data.get("clinical_note", ""),
            drug_database=obs_data.get("drug_database", ""),
            clinical_guidelines=obs_data.get("clinical_guidelines", ""),
            message=obs_data.get("message", ""),
            score_breakdown=obs_data.get("score_breakdown", {}),
            step_number=obs_data.get("step_number", 0),
            max_steps=obs_data.get("max_steps", 10),
            available_commands=obs_data.get("available_commands", []),
            metadata=obs_data.get("metadata", {}),
        )

        return StepResult(
            observation=observation,
            reward=payload.get("reward", 0.0),
            done=payload.get("done", False),
        )

    def _parse_state(self, payload: Dict) -> MedicalRecordState:
        """Parse server response into MedicalRecordState."""
        return MedicalRecordState(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
            task_id=payload.get("task_id", ""),
            note_id=payload.get("note_id", 0),
            submitted=payload.get("submitted", False),
            tools_called=payload.get("tools_called", []),
            current_score=payload.get("current_score", 0.0),
        )
