"""
Deterministic Grading System — Medical Record Abstraction Environment.

All graders:
  - Produce scores in (0.0, 1.0) exclusive
  - Are fully deterministic (same input → same output)
  - Use only Python stdlib (difflib for fuzzy matching)
  - Support partial credit via weighted component scoring

Task 1: Basic extraction (demographics, vitals)
Task 2: Entity extraction + validation (diagnoses, meds, conflicts)
Task 3: Risk assessment + clinical reasoning (risk level, flags, ROUGE-L)
"""

from __future__ import annotations

import difflib
import json
import re
from typing import Any

# ─── Import ontology for synonym resolution ───
try:
    from ..data.medical_ontology import resolve_to_canonical
except ImportError:
    from data.medical_ontology import resolve_to_canonical


# ═══════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def normalize(text: str) -> str:
    """Lowercase, strip, collapse whitespace."""
    return re.sub(r"\s+", " ", text.lower().strip())


def fuzzy_match(a: str, b: str, threshold: float = 0.7) -> float:
    """Return difflib SequenceMatcher ratio between two strings.

    Returns the ratio (0.0–1.0). If below threshold, returns 0.0.
    """
    ratio = difflib.SequenceMatcher(None, normalize(a), normalize(b)).ratio()
    return ratio if ratio >= threshold else 0.0


def medical_synonym_match(a: str, b: str) -> bool:
    """Check if two terms resolve to the same canonical condition.

    Handles canonical names with underscores (e.g. 'diabetes_mellitus_type_2')
    as well as natural language forms ('type 2 diabetes', 'HTN').
    """
    # Try direct resolution
    canon_a = resolve_to_canonical(a) or resolve_to_canonical(a.replace("_", " "))
    canon_b = resolve_to_canonical(b) or resolve_to_canonical(b.replace("_", " "))
    if canon_a and canon_b:
        return canon_a == canon_b
    # If one resolved and the other is already the canonical key
    if canon_a and b.replace(" ", "_").lower() == canon_a:
        return True
    if canon_b and a.replace(" ", "_").lower() == canon_b:
        return True
    # Fallback to fuzzy match
    return fuzzy_match(a, b, threshold=0.8) > 0


def compute_f1(
    predicted: list[str],
    ground_truth: list[str],
    match_fn=None,
) -> float:
    """Compute entity-level F1 score.

    Args:
        predicted: list of predicted entity strings
        ground_truth: list of ground truth entity strings
        match_fn: function(a, b) -> bool for matching. Defaults to exact match.

    Returns:
        F1 score in [0.0, 1.0]
    """
    if match_fn is None:
        match_fn = lambda a, b: normalize(a) == normalize(b)

    if not predicted and not ground_truth:
        return 1.0
    if not predicted or not ground_truth:
        return 0.0

    gt_matched = [False] * len(ground_truth)
    tp = 0

    for pred in predicted:
        for i, gt in enumerate(ground_truth):
            if not gt_matched[i] and match_fn(pred, gt):
                tp += 1
                gt_matched[i] = True
                break

    precision = tp / len(predicted) if predicted else 0.0
    recall = tp / len(ground_truth) if ground_truth else 0.0

    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def _lcs_length(a: list[str], b: list[str]) -> int:
    """Compute length of Longest Common Subsequence (dynamic programming)."""
    m, n = len(a), len(b)
    # Space-optimized: only need two rows
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, [0] * (n + 1)
    return prev[n]


def rouge_l(candidate: str, reference: str) -> float:
    """Compute ROUGE-L F1 score between candidate and reference text.

    Based on Longest Common Subsequence at the word level.
    Pure Python implementation — no external dependencies.

    Returns:
        ROUGE-L F1 score in [0.0, 1.0]
    """
    words_c = normalize(candidate).split()
    words_r = normalize(reference).split()

    if not words_c or not words_r:
        return 0.0

    lcs_len = _lcs_length(words_c, words_r)
    precision = lcs_len / len(words_c)
    recall = lcs_len / len(words_r)

    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def _safe_parse_json(data: str) -> dict | None:
    """Try to parse JSON from a string, handling markdown code fences."""
    text = data.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first and last lines (``` markers)
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return None


# ═══════════════════════════════════════════════════════════════
# TASK 1 GRADER: Basic Clinical Extraction
# ═══════════════════════════════════════════════════════════════

def grade_task_1(submission: dict, ground_truth: dict) -> tuple[float, dict[str, float]]:
    """Grade Task 1: demographics, chief complaint, vital signs.

    Component weights:
        patient_name:     0.15
        age:              0.10
        sex:              0.10
        chief_complaint:  0.20
        onset_date:       0.15
        vital_signs:      0.30 (6% each for 5 sub-fields)

    Returns:
        (total_score, breakdown_dict) where total_score in [0.0, 1.0]
    """
    breakdown: dict[str, float] = {}

    # Patient name (0.15) — normalized exact match
    gt_name = normalize(ground_truth.get("patient_name", ""))
    pred_name = normalize(submission.get("patient_name", ""))
    if gt_name and pred_name:
        breakdown["patient_name"] = fuzzy_match(pred_name, gt_name, threshold=0.85)
    else:
        breakdown["patient_name"] = 0.0

    # Age (0.10) — exact numeric match
    gt_age = ground_truth.get("age")
    pred_age = submission.get("age")
    try:
        breakdown["age"] = 1.0 if int(pred_age) == int(gt_age) else 0.0
    except (TypeError, ValueError):
        breakdown["age"] = 0.0

    # Sex (0.10) — normalized match
    gt_sex = normalize(str(ground_truth.get("sex", "")))
    pred_sex = normalize(str(submission.get("sex", "")))
    breakdown["sex"] = 1.0 if gt_sex and pred_sex and gt_sex[0] == pred_sex[0] else 0.0

    # Chief complaint (0.20) — fuzzy string match
    gt_cc = ground_truth.get("chief_complaint", "")
    pred_cc = submission.get("chief_complaint", "")
    if gt_cc and pred_cc:
        breakdown["chief_complaint"] = fuzzy_match(str(pred_cc), str(gt_cc), threshold=0.5)
    else:
        breakdown["chief_complaint"] = 0.0

    # Onset date (0.15) — exact match or close
    gt_date = normalize(str(ground_truth.get("onset_date", "")))
    pred_date = normalize(str(submission.get("onset_date", "")))
    if gt_date and pred_date:
        # Accept if the date string is contained or matches closely
        if gt_date == pred_date:
            breakdown["onset_date"] = 1.0
        elif gt_date in pred_date or pred_date in gt_date:
            breakdown["onset_date"] = 0.8
        else:
            breakdown["onset_date"] = fuzzy_match(pred_date, gt_date, threshold=0.6)
    else:
        breakdown["onset_date"] = 0.0

    # Vital signs (0.30) — 5 sub-fields, 0.06 each
    gt_vitals = ground_truth.get("vital_signs", {})
    pred_vitals = submission.get("vital_signs", {})
    if isinstance(pred_vitals, str):
        pred_vitals = _safe_parse_json(pred_vitals) or {}

    vital_scores: dict[str, float] = {}

    # Blood pressure — string match
    gt_bp = normalize(str(gt_vitals.get("blood_pressure", "")))
    pred_bp = normalize(str(pred_vitals.get("blood_pressure", "")))
    # Extract numbers from BP strings for comparison
    gt_bp_nums = re.findall(r"\d+", gt_bp)
    pred_bp_nums = re.findall(r"\d+", pred_bp)
    vital_scores["blood_pressure"] = 1.0 if gt_bp_nums == pred_bp_nums and gt_bp_nums else 0.0

    # Heart rate — ±2 tolerance
    vital_scores["heart_rate"] = _numeric_tolerance(
        pred_vitals.get("heart_rate"), gt_vitals.get("heart_rate"), tolerance=2
    )

    # Temperature — ±0.5 tolerance
    vital_scores["temperature"] = _numeric_tolerance(
        pred_vitals.get("temperature"), gt_vitals.get("temperature"), tolerance=0.5
    )

    # Respiratory rate — ±1 tolerance
    vital_scores["respiratory_rate"] = _numeric_tolerance(
        pred_vitals.get("respiratory_rate"), gt_vitals.get("respiratory_rate"), tolerance=1
    )

    # SpO2 — ±1 tolerance
    vital_scores["spo2"] = _numeric_tolerance(
        pred_vitals.get("spo2"), gt_vitals.get("spo2"), tolerance=1
    )

    breakdown["vital_signs"] = sum(vital_scores.values()) / 5.0 if vital_scores else 0.0

    # Weighted total
    weights = {
        "patient_name": 0.15,
        "age": 0.10,
        "sex": 0.10,
        "chief_complaint": 0.20,
        "onset_date": 0.15,
        "vital_signs": 0.30,
    }

    total = sum(breakdown[k] * weights[k] for k in weights)
    return round(total, 4), {k: round(v, 4) for k, v in breakdown.items()}


def _numeric_tolerance(pred, gt, tolerance: float) -> float:
    """Score 1.0 if pred is within tolerance of gt, else 0.0."""
    try:
        return 1.0 if abs(float(pred) - float(gt)) <= tolerance else 0.0
    except (TypeError, ValueError):
        return 0.0


# ═══════════════════════════════════════════════════════════════
# TASK 2 GRADER: Clinical Entity Extraction + Validation
# ═══════════════════════════════════════════════════════════════

def grade_task_2(submission: dict, ground_truth: dict) -> tuple[float, dict[str, float]]:
    """Grade Task 2: diagnoses, medications, inconsistencies.

    Component weights:
        diagnoses_f1:      0.25
        icd_accuracy:      0.15
        medications_f1:    0.15
        inconsistencies:   0.30
        allergies:         0.05
        format_validity:   0.10

    Returns:
        (total_score, breakdown_dict) where total_score in [0.0, 1.0]
    """
    breakdown: dict[str, float] = {}

    # Format validity (0.10)
    required_keys = {"diagnoses", "medications"}
    present_keys = set(submission.keys()) & required_keys
    breakdown["format_validity"] = len(present_keys) / len(required_keys)

    # Diagnoses F1 (0.25) — entity-level with synonym matching
    gt_diags = [d["condition"] for d in ground_truth.get("diagnoses", [])]
    pred_diags_raw = submission.get("diagnoses", [])
    pred_diags = []
    for d in pred_diags_raw:
        if isinstance(d, dict):
            pred_diags.append(d.get("condition", ""))
        elif isinstance(d, str):
            pred_diags.append(d)

    breakdown["diagnoses_f1"] = compute_f1(pred_diags, gt_diags, medical_synonym_match)

    # ICD-10 accuracy (0.15) — per matched diagnosis
    gt_icd_map = {d["condition"]: d["icd_code"] for d in ground_truth.get("diagnoses", [])}
    pred_icd_map = {}
    for d in pred_diags_raw:
        if isinstance(d, dict) and "condition" in d and "icd_code" in d:
            pred_icd_map[d["condition"]] = d["icd_code"]

    if gt_icd_map:
        icd_correct = 0
        icd_total = 0
        for gt_cond, gt_code in gt_icd_map.items():
            # Find matching predicted condition
            for pred_cond, pred_code in pred_icd_map.items():
                if medical_synonym_match(pred_cond, gt_cond):
                    icd_total += 1
                    if normalize(pred_code) == normalize(gt_code):
                        icd_correct += 1
                    break
            else:
                icd_total += 1  # Missing prediction counts against accuracy
        breakdown["icd_accuracy"] = icd_correct / icd_total if icd_total > 0 else 0.0
    else:
        breakdown["icd_accuracy"] = 1.0

    # Medications F1 (0.15) — drug name matching
    gt_meds = [m["drug"] for m in ground_truth.get("medications", [])]
    pred_meds_raw = submission.get("medications", [])
    pred_meds = []
    for m in pred_meds_raw:
        if isinstance(m, dict):
            pred_meds.append(m.get("drug", ""))
        elif isinstance(m, str):
            pred_meds.append(m)

    breakdown["medications_f1"] = compute_f1(
        pred_meds, gt_meds,
        lambda a, b: fuzzy_match(a, b, threshold=0.75) > 0
    )

    # Allergies (0.05) — recall of mentioned allergies
    gt_allergies = set(normalize(a) for a in ground_truth.get("allergies_mentioned", []))
    pred_allergies = set(
        normalize(a) if isinstance(a, str) else normalize(str(a))
        for a in submission.get("allergies_mentioned", [])
    )
    if gt_allergies:
        breakdown["allergies"] = len(gt_allergies & pred_allergies) / len(gt_allergies)
    else:
        breakdown["allergies"] = 1.0 if not pred_allergies else 0.5

    # Inconsistency detection (0.30) — recall of planted conflicts
    gt_inconsistencies = ground_truth.get("inconsistencies", [])
    pred_inconsistencies = submission.get("inconsistencies", [])

    if gt_inconsistencies:
        detected = 0
        for gt_inc in gt_inconsistencies:
            gt_desc = normalize(gt_inc.get("description", ""))
            gt_drug = normalize(gt_inc.get("drug", gt_inc.get("drug_a", "")))
            for pred_inc in pred_inconsistencies:
                pred_desc = normalize(str(pred_inc.get("description", "")))
                pred_drug = normalize(str(pred_inc.get("drug", pred_inc.get("drug_a", ""))))
                # Match if drug name matches OR description is similar
                if (fuzzy_match(gt_drug, pred_drug, threshold=0.7) > 0 or
                        fuzzy_match(gt_desc, pred_desc, threshold=0.4) > 0):
                    detected += 1
                    break
        breakdown["inconsistencies"] = detected / len(gt_inconsistencies)
    else:
        # No inconsistencies expected
        breakdown["inconsistencies"] = 1.0 if not pred_inconsistencies else 0.5

    # Weighted total
    weights = {
        "diagnoses_f1": 0.25,
        "icd_accuracy": 0.15,
        "medications_f1": 0.15,
        "inconsistencies": 0.30,
        "allergies": 0.05,
        "format_validity": 0.10,
    }

    total = sum(breakdown.get(k, 0) * weights[k] for k in weights)
    return round(total, 4), {k: round(v, 4) for k, v in breakdown.items()}


# ═══════════════════════════════════════════════════════════════
# TASK 3 GRADER: Risk Assessment + Clinical Reasoning
# ═══════════════════════════════════════════════════════════════

def grade_task_3(submission: dict, ground_truth: dict) -> tuple[float, dict[str, float]]:
    """Grade Task 3: risk level, critical flags, readmission score, summary.

    Component weights:
        risk_level:             0.20
        risk_factors:           0.15
        critical_flags:         0.25
        readmission_risk_score: 0.15
        clinical_summary:       0.25

    Returns:
        (total_score, breakdown_dict) where total_score in [0.0, 1.0]
    """
    breakdown: dict[str, float] = {}

    # Risk level (0.20) — exact match (high/medium/low)
    gt_risk = normalize(str(ground_truth.get("risk_level", "")))
    pred_risk = normalize(str(submission.get("risk_level", "")))
    breakdown["risk_level"] = 1.0 if gt_risk and pred_risk and gt_risk == pred_risk else 0.0

    # Risk factors (0.15) — fuzzy recall
    gt_factors = ground_truth.get("risk_factors", [])
    pred_factors = submission.get("risk_factors", [])
    if isinstance(pred_factors, str):
        pred_factors = [f.strip() for f in pred_factors.split(",")]

    if gt_factors:
        detected = 0
        for gt_f in gt_factors:
            gt_norm = normalize(str(gt_f))
            for pred_f in pred_factors:
                pred_norm = normalize(str(pred_f))
                if fuzzy_match(gt_norm, pred_norm, threshold=0.5) > 0:
                    detected += 1
                    break
        breakdown["risk_factors"] = detected / len(gt_factors)
    else:
        breakdown["risk_factors"] = 1.0 if not pred_factors else 0.5

    # Critical flags (0.25) — recall of planted flags
    gt_flags = ground_truth.get("critical_flags", [])
    pred_flags = submission.get("critical_flags", [])

    if gt_flags:
        detected = 0
        for gt_flag in gt_flags:
            gt_flag_text = normalize(gt_flag.get("flag", ""))
            for pred_flag in pred_flags:
                if isinstance(pred_flag, dict):
                    pred_flag_text = normalize(pred_flag.get("flag", ""))
                else:
                    pred_flag_text = normalize(str(pred_flag))
                if fuzzy_match(gt_flag_text, pred_flag_text, threshold=0.4) > 0:
                    detected += 1
                    break
        breakdown["critical_flags"] = detected / len(gt_flags)
    else:
        # No critical flags expected (low-risk patient)
        breakdown["critical_flags"] = 1.0 if not pred_flags else 0.5

    # Readmission risk score (0.15) — proximity
    gt_readmit = ground_truth.get("readmission_risk_score", 0.5)
    pred_readmit = submission.get("readmission_risk_score")
    try:
        pred_readmit = float(pred_readmit)
        error = abs(pred_readmit - gt_readmit)
        breakdown["readmission_risk_score"] = max(0.0, 1.0 - error / 0.5)
    except (TypeError, ValueError):
        breakdown["readmission_risk_score"] = 0.0

    # Clinical summary (0.25) — ROUGE-L
    gt_summary = str(ground_truth.get("clinical_summary", ""))
    pred_summary = str(submission.get("clinical_summary", ""))
    if gt_summary and pred_summary:
        breakdown["clinical_summary"] = rouge_l(pred_summary, gt_summary)
    else:
        breakdown["clinical_summary"] = 0.0

    # Weighted total
    weights = {
        "risk_level": 0.20,
        "risk_factors": 0.15,
        "critical_flags": 0.25,
        "readmission_risk_score": 0.15,
        "clinical_summary": 0.25,
    }

    total = sum(breakdown.get(k, 0) * weights[k] for k in weights)
    return round(total, 4), {k: round(v, 4) for k, v in breakdown.items()}


# ═══════════════════════════════════════════════════════════════
# MAIN GRADING DISPATCHER
# ═══════════════════════════════════════════════════════════════

GRADERS = {
    "task_1": grade_task_1,
    "task_2": grade_task_2,
    "task_3": grade_task_3,
}


def grade_submission(
    task_id: str,
    raw_submission: str,
    ground_truth: dict[str, Any],
) -> tuple[float, dict[str, float]]:
    """Grade a raw JSON submission string against ground truth.

    Args:
        task_id: "task_1", "task_2", or "task_3"
        raw_submission: JSON string from the agent
        ground_truth: Ground truth dict from the note bank

    Returns:
        (score, breakdown) where score is in (0.0, 1.0) exclusive
    """
    grader = GRADERS.get(task_id)
    if not grader:
        return 0.01, {"error": 1.0}

    parsed = _safe_parse_json(raw_submission)
    if parsed is None:
        return 0.01, {"parse_error": 1.0}

    score, breakdown = grader(parsed, ground_truth)
    # Clamp to strictly (0, 1) — validator rejects exactly 0.0 and 1.0
    score = max(0.01, min(0.99, score))
    return score, breakdown
