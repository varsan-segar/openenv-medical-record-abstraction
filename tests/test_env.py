"""Tests for the Medical Record Abstraction Environment."""
import sys
import json
import pytest

sys.path.insert(0, ".")

from server.environment import MedicalRecordEnvironment
from models import MedicalRecordAction, MedicalRecordObservation, MedicalRecordState


class TestEnvironmentReset:
    """Test environment reset behavior."""

    def test_reset_defaults(self):
        env = MedicalRecordEnvironment()
        obs = env.reset()
        assert isinstance(obs, MedicalRecordObservation)
        assert not obs.done
        assert obs.reward == 0.0
        assert obs.task_id == "task_1"
        assert obs.step_number == 0
        assert len(obs.available_commands) > 0

    def test_reset_task_1(self):
        env = MedicalRecordEnvironment()
        obs = env.reset(task_id="task_1", note_id=0)
        assert obs.task_id == "task_1"
        assert obs.max_steps == 5
        assert "get_task" in obs.available_commands
        assert "get_drugs" not in obs.available_commands

    def test_reset_task_2(self):
        env = MedicalRecordEnvironment()
        obs = env.reset(task_id="task_2", note_id=0)
        assert obs.task_id == "task_2"
        assert obs.max_steps == 8
        assert "get_drugs" in obs.available_commands

    def test_reset_task_3(self):
        env = MedicalRecordEnvironment()
        obs = env.reset(task_id="task_3", note_id=0)
        assert obs.task_id == "task_3"
        assert obs.max_steps == 10
        assert "get_guidelines" in obs.available_commands

    def test_reset_invalid_task_defaults(self):
        env = MedicalRecordEnvironment()
        obs = env.reset(task_id="invalid_task")
        assert obs.task_id == "task_1"

    def test_reset_clears_state(self):
        env = MedicalRecordEnvironment()
        env.reset(task_id="task_1", note_id=0)
        env.step(MedicalRecordAction(command="get_task"))
        env.step(MedicalRecordAction(command="submit", data="{}"))
        assert env.state.submitted

        obs = env.reset(task_id="task_1", note_id=0)
        assert not env.state.submitted
        assert env.state.step_count == 0
        assert env.state.current_score == 0.0


class TestEnvironmentStep:
    """Test environment step behavior."""

    def test_get_task(self):
        env = MedicalRecordEnvironment()
        env.reset(task_id="task_1", note_id=0)
        obs = env.step(MedicalRecordAction(command="get_task"))
        assert not obs.done
        assert obs.task_description != ""
        assert obs.reward > 0  # exploration reward

    def test_get_note(self):
        env = MedicalRecordEnvironment()
        env.reset(task_id="task_1", note_id=0)
        obs = env.step(MedicalRecordAction(command="get_note"))
        assert not obs.done
        assert obs.clinical_note != ""
        assert "PATIENT:" in obs.clinical_note

    def test_get_drugs_task2(self):
        env = MedicalRecordEnvironment()
        env.reset(task_id="task_2", note_id=0)
        obs = env.step(MedicalRecordAction(command="get_drugs"))
        assert not obs.done
        assert obs.drug_database != ""

    def test_get_drugs_unavailable_task1(self):
        env = MedicalRecordEnvironment()
        env.reset(task_id="task_1", note_id=0)
        obs = env.step(MedicalRecordAction(command="get_drugs"))
        assert not obs.done
        assert obs.drug_database == ""
        assert obs.reward < 0

    def test_get_guidelines_task3(self):
        env = MedicalRecordEnvironment()
        env.reset(task_id="task_3", note_id=0)
        obs = env.step(MedicalRecordAction(command="get_guidelines"))
        assert not obs.done
        assert obs.clinical_guidelines != ""

    def test_submit_valid_json(self):
        env = MedicalRecordEnvironment()
        env.reset(task_id="task_1", note_id=0)
        submission = json.dumps({"patient_name": "Test", "age": 50, "sex": "Male"})
        obs = env.step(MedicalRecordAction(command="submit", data=submission))
        assert obs.done
        assert len(obs.score_breakdown) > 0

    def test_submit_invalid_json(self):
        env = MedicalRecordEnvironment()
        env.reset(task_id="task_1", note_id=0)
        obs = env.step(MedicalRecordAction(command="submit", data="not json"))
        assert obs.done
        assert obs.reward < 0
        assert "parse_error" in obs.score_breakdown

    def test_submit_perfect_task1(self):
        env = MedicalRecordEnvironment()
        env.reset(task_id="task_1", note_id=0)
        perfect = {
            "patient_name": "Maria Rodriguez", "age": 52, "sex": "Female",
            "chief_complaint": "Persistent headache for 3 days",
            "onset_date": "2024-03-12",
            "vital_signs": {"blood_pressure": "158/94", "heart_rate": 78,
                            "temperature": 98.6, "respiratory_rate": 16, "spo2": 98},
        }
        obs = env.step(MedicalRecordAction(command="submit", data=json.dumps(perfect)))
        assert obs.done
        assert obs.reward >= 0.95

    def test_unknown_command(self):
        env = MedicalRecordEnvironment()
        env.reset(task_id="task_1", note_id=0)
        obs = env.step(MedicalRecordAction(command="fly_to_moon"))
        assert not obs.done
        assert obs.reward < 0

    def test_step_after_submit(self):
        env = MedicalRecordEnvironment()
        env.reset(task_id="task_1", note_id=0)
        env.step(MedicalRecordAction(command="submit", data="{}"))
        obs = env.step(MedicalRecordAction(command="get_note"))
        assert obs.done  # Should remain done

    def test_step_count_increments(self):
        env = MedicalRecordEnvironment()
        env.reset(task_id="task_1", note_id=0)
        env.step(MedicalRecordAction(command="get_task"))
        env.step(MedicalRecordAction(command="get_note"))
        assert env.state.step_count == 2


class TestEnvironmentState:
    """Test state tracking."""

    def test_state_type(self):
        env = MedicalRecordEnvironment()
        env.reset(task_id="task_1", note_id=0)
        state = env.state
        assert isinstance(state, MedicalRecordState)

    def test_state_tracks_tools(self):
        env = MedicalRecordEnvironment()
        env.reset(task_id="task_2", note_id=0)
        env.step(MedicalRecordAction(command="get_task"))
        env.step(MedicalRecordAction(command="get_note"))
        env.step(MedicalRecordAction(command="get_drugs"))
        state = env.state
        assert "get_task" in state.tools_called
        assert "get_note" in state.tools_called
        assert "get_drugs" in state.tools_called

    def test_state_tracks_submission(self):
        env = MedicalRecordEnvironment()
        env.reset(task_id="task_1", note_id=0)
        assert not env.state.submitted
        env.step(MedicalRecordAction(command="submit", data="{}"))
        assert env.state.submitted

    def test_episode_id_changes_on_reset(self):
        env = MedicalRecordEnvironment()
        env.reset(task_id="task_1")
        id1 = env.state.episode_id
        env.reset(task_id="task_1")
        id2 = env.state.episode_id
        assert id1 != id2


class TestAllNotes:
    """Test that all 24 notes can be loaded and processed."""

    @pytest.mark.parametrize("task_id", ["task_1", "task_2", "task_3"])
    def test_all_notes_load(self, task_id):
        env = MedicalRecordEnvironment()
        for note_id in range(8):
            obs = env.reset(task_id=task_id, note_id=note_id)
            assert obs.task_id == task_id
            note_obs = env.step(MedicalRecordAction(command="get_note"))
            assert note_obs.clinical_note != ""
            assert "PATIENT:" in note_obs.clinical_note
