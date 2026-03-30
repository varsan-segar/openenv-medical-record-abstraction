"""
Task Definitions — Medical Record Abstraction Environment.

Defines the three tasks (easy → medium → hard) with their configurations,
available commands, max steps, descriptions, and output schemas.
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════
# TASK CONFIGURATIONS
# ═══════════════════════════════════════════════════════════════

TASK_CONFIGS: dict[str, dict] = {
    "task_1": {
        "name": "Basic Clinical Extraction",
        "difficulty": "easy",
        "max_steps": 5,
        "available_commands": ["get_task", "get_note", "submit"],
        "description": (
            "TASK: Basic Clinical Extraction (Easy)\n\n"
            "Extract the following information from the clinical note:\n"
            "- Patient demographics (name, age, sex)\n"
            "- Chief complaint\n"
            "- Onset date (calculate from the note date and duration mentioned)\n"
            "- Vital signs (blood pressure, heart rate, temperature, "
            "respiratory rate, SpO2)\n\n"
            "REQUIRED OUTPUT FORMAT (JSON):\n"
            "{\n"
            '  "patient_name": "string",\n'
            '  "age": integer,\n'
            '  "sex": "Male" or "Female",\n'
            '  "chief_complaint": "string",\n'
            '  "onset_date": "YYYY-MM-DD",\n'
            '  "vital_signs": {\n'
            '    "blood_pressure": "systolic/diastolic",\n'
            '    "heart_rate": integer,\n'
            '    "temperature": float,\n'
            '    "respiratory_rate": integer,\n'
            '    "spo2": integer\n'
            "  }\n"
            "}\n\n"
            "SCORING: Name (15%), Age (10%), Sex (10%), Chief complaint (20%), "
            "Onset date (15%), Vital signs (30%)"
        ),
    },
    "task_2": {
        "name": "Clinical Entity Extraction + Validation",
        "difficulty": "medium",
        "max_steps": 8,
        "available_commands": ["get_task", "get_note", "get_drugs", "submit"],
        "description": (
            "TASK: Clinical Entity Extraction + Validation (Medium)\n\n"
            "Extract clinical entities AND cross-reference with the drug "
            "interaction database to detect safety issues:\n"
            "- Diagnoses with ICD-10 codes\n"
            "- Medications with dosages and indications\n"
            "- Allergies mentioned in the note\n"
            "- Drug-allergy conflicts and drug-drug interactions\n\n"
            "Use the 'get_drugs' command to access the drug interaction database.\n\n"
            "REQUIRED OUTPUT FORMAT (JSON):\n"
            "{\n"
            '  "diagnoses": [\n'
            '    {"condition": "canonical_name", "icd_code": "X00.0"}\n'
            "  ],\n"
            '  "medications": [\n'
            '    {"drug": "name", "dosage": "dose frequency", '
            '"indication": "reason"}\n'
            "  ],\n"
            '  "allergies_mentioned": ["allergy1", "allergy2"],\n'
            '  "inconsistencies": [\n'
            '    {"type": "drug_allergy_conflict" or "drug_drug_interaction",\n'
            '     "drug": "name" or "drug_a": "name",\n'
            '     "severity": "high" or "medium",\n'
            '     "description": "explanation"}\n'
            "  ]\n"
            "}\n\n"
            "SCORING: Diagnoses F1 (25%), ICD-10 accuracy (15%), "
            "Medications F1 (15%), Inconsistency detection (30%), "
            "Allergies (5%), Format (10%)"
        ),
    },
    "task_3": {
        "name": "Risk Assessment + Clinical Reasoning",
        "difficulty": "hard",
        "max_steps": 10,
        "available_commands": [
            "get_task", "get_note", "get_drugs", "get_guidelines", "submit",
        ],
        "description": (
            "TASK: Risk Assessment + Clinical Reasoning (Hard)\n\n"
            "Perform a comprehensive clinical risk assessment:\n"
            "- Determine overall risk level\n"
            "- Identify specific risk factors from the clinical data\n"
            "- Flag critical safety concerns requiring immediate action\n"
            "- Estimate 30-day readmission risk\n"
            "- Generate a clinical summary\n\n"
            "Use 'get_drugs' for the drug interaction database and "
            "'get_guidelines' for clinical risk assessment guidelines.\n\n"
            "REQUIRED OUTPUT FORMAT (JSON):\n"
            "{\n"
            '  "risk_level": "high" or "medium" or "low",\n'
            '  "risk_factors": ["factor1", "factor2", ...],\n'
            '  "critical_flags": [\n'
            '    {"flag": "description", "action": "recommended action", '
            '"urgency": "immediate" or "urgent"}\n'
            "  ],\n"
            '  "readmission_risk_score": float (0.0 to 1.0),\n'
            '  "clinical_summary": "2-4 sentence summary"\n'
            "}\n\n"
            "SCORING: Risk level (20%), Risk factors (15%), "
            "Critical flags (25%), Readmission score (15%), "
            "Clinical summary ROUGE-L (25%)"
        ),
    },
}


# ═══════════════════════════════════════════════════════════════
# CLINICAL GUIDELINES (for Task 3)
# ═══════════════════════════════════════════════════════════════

CLINICAL_GUIDELINES = """\
=== CLINICAL RISK ASSESSMENT GUIDELINES ===

1. RISK LEVEL CLASSIFICATION
   - HIGH: Any of the following: ICU-level vitals (SpO2 <90%, SBP <90, \
HR >120), active organ failure, sepsis (lactate >2.0), \
acute coronary syndrome, respiratory failure
   - MEDIUM: Abnormal but stable vitals, chronic disease exacerbation, \
moderate lab abnormalities, 1+ hospitalization in past 90 days
   - LOW: Stable vitals, well-controlled chronic conditions, \
routine follow-up, no acute concerns

2. CRITICAL FLAGS (require immediate/urgent action)
   - Hyperkalemia (K+ >5.5): calcium gluconate, insulin/glucose
   - Supratherapeutic INR (>3.5): hold warfarin, vitamin K consideration
   - Severe hypoglycemia (glucose <60): IV dextrose, hold oral hypoglycemics
   - Sepsis (lactate >2.0 + infection): fluid resuscitation, antibiotics
   - Acute respiratory failure: supplemental O2, BiPAP/intubation evaluation
   - Hypotension (SBP <90): fluid bolus, vasopressor consideration
   - Drug contraindications: metformin with eGFR <30, NSAIDs with AKI

3. READMISSION RISK FACTORS
   - Prior admissions: 2+ in 30 days (high), 1 in 30 days (medium)
   - Functional status: nursing home resident, advanced dementia
   - Disease severity: low EF (<30%), MELD >20, eGFR <30
   - Social factors: medication non-adherence, limited support
   - Comorbidity burden: 5+ active conditions

4. READMISSION RISK SCORING (0.0 to 1.0)
   - 0.0-0.2: Low risk (stable, well-controlled, good support)
   - 0.2-0.5: Moderate risk (some risk factors present)
   - 0.5-0.8: High risk (multiple risk factors, recent admissions)
   - 0.8-1.0: Very high risk (critical illness, frequent readmissions)

5. CLINICAL SUMMARY REQUIREMENTS
   - 2-4 sentences capturing key clinical picture
   - Include: primary diagnosis, severity, key risk factors
   - Note: critical medication concerns, recommended next steps
   - Mention: readmission risk drivers
"""


def get_task_config(task_id: str) -> dict | None:
    """Get task configuration by task_id."""
    return TASK_CONFIGS.get(task_id)


def get_task_description(task_id: str) -> str:
    """Get the human-readable task description."""
    config = TASK_CONFIGS.get(task_id)
    return config["description"] if config else "Unknown task."


def get_available_commands(task_id: str) -> list[str]:
    """Get the list of available commands for a task."""
    config = TASK_CONFIGS.get(task_id)
    return config["available_commands"] if config else []


def get_max_steps(task_id: str) -> int:
    """Get the maximum steps allowed for a task."""
    config = TASK_CONFIGS.get(task_id)
    return config["max_steps"] if config else 10
