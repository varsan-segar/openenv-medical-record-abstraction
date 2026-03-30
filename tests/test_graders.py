"""Tests for the grading system."""
import sys
import json
import pytest

sys.path.insert(0, ".")

from server.graders import (
    grade_task_1, grade_task_2, grade_task_3,
    grade_submission, fuzzy_match, rouge_l, compute_f1,
    medical_synonym_match, normalize,
)


class TestUtilities:
    """Test utility functions."""

    def test_normalize(self):
        assert normalize("  Hello   World  ") == "hello world"

    def test_fuzzy_match_identical(self):
        assert fuzzy_match("hello", "hello") == 1.0

    def test_fuzzy_match_below_threshold(self):
        assert fuzzy_match("abc", "xyz") == 0.0

    def test_medical_synonym_htn(self):
        assert medical_synonym_match("HTN", "hypertension")

    def test_medical_synonym_mi(self):
        assert medical_synonym_match("heart attack", "myocardial infarction")

    def test_medical_synonym_no_match(self):
        assert not medical_synonym_match("diabetes", "hypertension")

    def test_rouge_l_identical(self):
        assert rouge_l("the cat sat", "the cat sat") == 1.0

    def test_rouge_l_empty(self):
        assert rouge_l("", "the cat sat") == 0.0

    def test_rouge_l_partial(self):
        score = rouge_l("the cat on mat", "the cat sat on the mat")
        assert 0.5 < score < 1.0

    def test_f1_perfect(self):
        assert compute_f1(["a", "b", "c"], ["a", "b", "c"]) == 1.0

    def test_f1_empty_both(self):
        assert compute_f1([], []) == 1.0

    def test_f1_empty_pred(self):
        assert compute_f1([], ["a"]) == 0.0

    def test_f1_partial(self):
        f1 = compute_f1(["a", "b"], ["a", "b", "c"])
        assert 0.5 < f1 < 1.0


class TestTask1Grader:
    """Test Task 1 grading."""

    GT = {
        "patient_name": "Maria Rodriguez", "age": 52, "sex": "Female",
        "chief_complaint": "Persistent headache for 3 days",
        "onset_date": "2024-03-12",
        "vital_signs": {"blood_pressure": "158/94", "heart_rate": 78,
                        "temperature": 98.6, "respiratory_rate": 16, "spo2": 98},
    }

    def test_perfect_score(self):
        score, bd = grade_task_1(self.GT, self.GT)
        assert score == 1.0

    def test_empty_submission(self):
        score, bd = grade_task_1({}, self.GT)
        assert score == 0.0

    def test_partial_name(self):
        sub = {**self.GT, "patient_name": "Rodriguez"}
        score, bd = grade_task_1(sub, self.GT)
        assert 0.5 < score < 1.0

    def test_wrong_age(self):
        sub = {**self.GT, "age": 99}
        score, bd = grade_task_1(sub, self.GT)
        assert bd["age"] == 0.0
        assert score < 1.0

    def test_wrong_vitals(self):
        sub = {**self.GT, "vital_signs": {"blood_pressure": "120/80",
               "heart_rate": 60, "temperature": 97.0, "respiratory_rate": 10, "spo2": 100}}
        score, bd = grade_task_1(sub, self.GT)
        assert bd["vital_signs"] == 0.0


class TestTask2Grader:
    """Test Task 2 grading."""

    GT = {
        "diagnoses": [
            {"condition": "diabetes_mellitus_type_2", "icd_code": "E11.9"},
            {"condition": "hypertension", "icd_code": "I10"},
        ],
        "medications": [
            {"drug": "metformin", "dosage": "1000mg BID", "indication": "diabetes"},
        ],
        "allergies_mentioned": ["penicillin"],
        "inconsistencies": [
            {"type": "drug_allergy_conflict", "drug": "amoxicillin",
             "description": "Penicillin class cross-reactivity"},
        ],
    }

    def test_perfect_score(self):
        score, bd = grade_task_2(self.GT, self.GT)
        assert score >= 0.95

    def test_synonym_matching(self):
        sub = {**self.GT, "diagnoses": [
            {"condition": "type 2 diabetes", "icd_code": "E11.9"},
            {"condition": "HTN", "icd_code": "I10"},
        ]}
        score, bd = grade_task_2(sub, self.GT)
        assert bd["diagnoses_f1"] == 1.0

    def test_missing_inconsistencies(self):
        sub = {**self.GT, "inconsistencies": []}
        score, bd = grade_task_2(sub, self.GT)
        assert bd["inconsistencies"] == 0.0


class TestTask3Grader:
    """Test Task 3 grading."""

    GT = {
        "risk_level": "high",
        "risk_factors": ["EF 25%", "CKD stage 4"],
        "critical_flags": [
            {"flag": "Hyperkalemia K+ 5.8", "action": "Treat urgently", "urgency": "immediate"},
        ],
        "readmission_risk_score": 0.88,
        "clinical_summary": "High risk patient with heart failure and kidney disease.",
    }

    def test_perfect_risk_level(self):
        score, bd = grade_task_3(self.GT, self.GT)
        assert bd["risk_level"] == 1.0

    def test_wrong_risk_level(self):
        sub = {**self.GT, "risk_level": "low"}
        score, bd = grade_task_3(sub, self.GT)
        assert bd["risk_level"] == 0.0

    def test_readmission_close(self):
        sub = {**self.GT, "readmission_risk_score": 0.85}
        score, bd = grade_task_3(sub, self.GT)
        assert bd["readmission_risk_score"] > 0.9

    def test_readmission_far(self):
        sub = {**self.GT, "readmission_risk_score": 0.1}
        score, bd = grade_task_3(sub, self.GT)
        assert bd["readmission_risk_score"] < 0.5


class TestGradeSubmission:
    """Test the main grade_submission dispatcher."""

    def test_invalid_task(self):
        score, bd = grade_submission("task_99", "{}", {})
        assert score == 0.0

    def test_invalid_json(self):
        score, bd = grade_submission("task_1", "not json", {})
        assert score == 0.0
        assert "parse_error" in bd

    def test_deterministic(self):
        gt = {"patient_name": "Test", "age": 50, "sex": "Male"}
        s1, _ = grade_submission("task_1", json.dumps(gt), gt)
        s2, _ = grade_submission("task_1", json.dumps(gt), gt)
        assert s1 == s2

    def test_markdown_code_fence(self):
        gt = {"patient_name": "Test", "age": 50, "sex": "Male"}
        wrapped = '```json\n' + json.dumps(gt) + '\n```'
        score, bd = grade_submission("task_1", wrapped, gt)
        assert "parse_error" not in bd
