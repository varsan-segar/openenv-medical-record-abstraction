"""
Synthetic Clinical Notes — 24 pre-built notes with ground truth.

8 notes per task (easy/medium/hard), covering diverse medical specialties.
Each note includes the raw clinical text and complete ground truth for grading.
"""

from typing import Any


def get_note(task_id: str, note_id: int) -> dict[str, Any]:
    """Get a specific note by task and index."""
    notes = NOTES_BY_TASK.get(task_id, [])
    if 0 <= note_id < len(notes):
        return notes[note_id]
    return notes[note_id % len(notes)] if notes else {}


def get_all_notes_for_task(task_id: str) -> list[dict[str, Any]]:
    """Get all notes for a given task."""
    return NOTES_BY_TASK.get(task_id, [])


# ═══════════════════════════════════════════════════════════════
# TASK 1: Basic Clinical Extraction (Easy)
# Agent extracts: demographics, chief complaint, vital signs
# ═══════════════════════════════════════════════════════════════

TASK_1_NOTES: list[dict[str, Any]] = [
    {
        "id": "task1_note_001",
        "text": (
            "PATIENT: Maria Rodriguez, 52 y/o Female\n"
            "DATE: 2024-03-15\n"
            "CHIEF COMPLAINT: Persistent headache for 3 days\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Ms. Rodriguez presents with a 3-day history of bilateral frontal "
            "headaches, described as a constant pressure sensation rated 6/10. "
            "Pain is worse in the morning and improves slightly with ibuprofen. "
            "She denies visual changes, nausea, or vomiting. No recent head "
            "trauma. She has a history of untreated hypertension.\n\n"
            "VITAL SIGNS:\n"
            "BP: 158/94 mmHg | HR: 78 bpm | Temp: 98.6°F | RR: 16 | SpO2: 98%\n\n"
            "ASSESSMENT: Hypertensive urgency, tension-type headache\n"
            "PLAN: Amlodipine 5mg daily, follow-up in 1 week, "
            "headache diary recommended"
        ),
        "ground_truth": {
            "patient_name": "Maria Rodriguez",
            "age": 52,
            "sex": "Female",
            "chief_complaint": "Persistent headache for 3 days",
            "onset_date": "2024-03-12",
            "vital_signs": {
                "blood_pressure": "158/94",
                "heart_rate": 78,
                "temperature": 98.6,
                "respiratory_rate": 16,
                "spo2": 98,
            },
        },
    },
    {
        "id": "task1_note_002",
        "text": (
            "PATIENT: James Chen, 67 y/o Male\n"
            "DATE: 2024-04-02\n"
            "CHIEF COMPLAINT: Chest tightness with exertion for 2 weeks\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Mr. Chen reports progressive chest tightness occurring with moderate "
            "exertion such as climbing stairs, first noticed approximately 2 weeks "
            "ago. The sensation resolves with rest within 5 minutes. He denies "
            "chest pain at rest, orthopnea, or lower extremity edema. Known "
            "history of hyperlipidemia on atorvastatin.\n\n"
            "VITAL SIGNS:\n"
            "BP: 142/88 mmHg | HR: 82 bpm | Temp: 98.2°F | RR: 18 | SpO2: 96%\n\n"
            "ASSESSMENT: Stable angina, rule out ACS\n"
            "PLAN: Stress test, continue atorvastatin, add aspirin 81mg daily"
        ),
        "ground_truth": {
            "patient_name": "James Chen",
            "age": 67,
            "sex": "Male",
            "chief_complaint": "Chest tightness with exertion for 2 weeks",
            "onset_date": "2024-03-19",
            "vital_signs": {
                "blood_pressure": "142/88",
                "heart_rate": 82,
                "temperature": 98.2,
                "respiratory_rate": 18,
                "spo2": 96,
            },
        },
    },
    {
        "id": "task1_note_003",
        "text": (
            "PATIENT: Aisha Patel, 34 y/o Female\n"
            "DATE: 2024-05-10\n"
            "CHIEF COMPLAINT: Shortness of breath and wheezing for 1 day\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Ms. Patel presents with acute onset shortness of breath and audible "
            "wheezing that began yesterday evening after exposure to a neighbor's "
            "cat. She has a known history of asthma diagnosed in childhood but "
            "has been off controller medications for 2 years. She used her rescue "
            "inhaler 4 times since last night with partial relief.\n\n"
            "VITAL SIGNS:\n"
            "BP: 118/72 mmHg | HR: 102 bpm | Temp: 98.4°F | RR: 24 | SpO2: 93%\n\n"
            "ASSESSMENT: Acute asthma exacerbation\n"
            "PLAN: Nebulized albuterol, oral prednisone 40mg x 5 days, "
            "restart fluticasone inhaler"
        ),
        "ground_truth": {
            "patient_name": "Aisha Patel",
            "age": 34,
            "sex": "Female",
            "chief_complaint": "Shortness of breath and wheezing for 1 day",
            "onset_date": "2024-05-09",
            "vital_signs": {
                "blood_pressure": "118/72",
                "heart_rate": 102,
                "temperature": 98.4,
                "respiratory_rate": 24,
                "spo2": 93,
            },
        },
    },
    {
        "id": "task1_note_004",
        "text": (
            "PATIENT: Robert Williams, 71 y/o Male\n"
            "DATE: 2024-06-18\n"
            "CHIEF COMPLAINT: Left knee pain and swelling for 5 days\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Mr. Williams presents with progressively worsening left knee pain "
            "and swelling over the past 5 days. He describes the pain as a deep "
            "ache rated 7/10, worse with weight bearing and stairs. No recent "
            "injury or trauma. He has a history of bilateral knee osteoarthritis "
            "diagnosed 4 years ago. Current medications include acetaminophen PRN.\n\n"
            "VITAL SIGNS:\n"
            "BP: 134/82 mmHg | HR: 74 bpm | Temp: 98.8°F | RR: 14 | SpO2: 97%\n\n"
            "ASSESSMENT: Osteoarthritis flare, left knee\n"
            "PLAN: Knee X-ray, topical diclofenac, PT referral"
        ),
        "ground_truth": {
            "patient_name": "Robert Williams",
            "age": 71,
            "sex": "Male",
            "chief_complaint": "Left knee pain and swelling for 5 days",
            "onset_date": "2024-06-13",
            "vital_signs": {
                "blood_pressure": "134/82",
                "heart_rate": 74,
                "temperature": 98.8,
                "respiratory_rate": 14,
                "spo2": 97,
            },
        },
    },
    {
        "id": "task1_note_005",
        "text": (
            "PATIENT: Sarah Thompson, 45 y/o Female\n"
            "DATE: 2024-07-22\n"
            "CHIEF COMPLAINT: Epigastric burning and nausea for 10 days\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Ms. Thompson reports a 10-day history of epigastric burning pain "
            "that worsens after meals and when lying flat. She also notes "
            "intermittent nausea without vomiting. Symptoms began after she "
            "started taking ibuprofen daily for back pain 3 weeks ago. She "
            "denies melena, hematemesis, or weight loss. No prior GI history.\n\n"
            "VITAL SIGNS:\n"
            "BP: 122/76 mmHg | HR: 70 bpm | Temp: 98.6°F | RR: 16 | SpO2: 99%\n\n"
            "ASSESSMENT: NSAID-induced gastritis, rule out peptic ulcer\n"
            "PLAN: Discontinue ibuprofen, start omeprazole 20mg daily, "
            "H. pylori testing"
        ),
        "ground_truth": {
            "patient_name": "Sarah Thompson",
            "age": 45,
            "sex": "Female",
            "chief_complaint": "Epigastric burning and nausea for 10 days",
            "onset_date": "2024-07-12",
            "vital_signs": {
                "blood_pressure": "122/76",
                "heart_rate": 70,
                "temperature": 98.6,
                "respiratory_rate": 16,
                "spo2": 99,
            },
        },
    },
    {
        "id": "task1_note_006",
        "text": (
            "PATIENT: David Kim, 58 y/o Male\n"
            "DATE: 2024-08-05\n"
            "CHIEF COMPLAINT: Fatigue and increased thirst for 2 weeks\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Mr. Kim presents with a 2-week history of progressive fatigue, "
            "increased thirst, and frequent urination. He reports drinking 3-4 "
            "liters of water daily, up from his usual 1-2 liters. He has noticed "
            "unintentional weight loss of approximately 5 pounds. Family history "
            "is significant for type 2 diabetes in both parents.\n\n"
            "VITAL SIGNS:\n"
            "BP: 128/80 mmHg | HR: 88 bpm | Temp: 98.4°F | RR: 16 | SpO2: 98%\n\n"
            "ASSESSMENT: New-onset diabetes mellitus, likely type 2\n"
            "PLAN: Fasting glucose, HbA1c, BMP, start metformin 500mg BID"
        ),
        "ground_truth": {
            "patient_name": "David Kim",
            "age": 58,
            "sex": "Male",
            "chief_complaint": "Fatigue and increased thirst for 2 weeks",
            "onset_date": "2024-07-22",
            "vital_signs": {
                "blood_pressure": "128/80",
                "heart_rate": 88,
                "temperature": 98.4,
                "respiratory_rate": 16,
                "spo2": 98,
            },
        },
    },
    {
        "id": "task1_note_007",
        "text": (
            "PATIENT: Linda Okonkwo, 29 y/o Female\n"
            "DATE: 2024-09-14\n"
            "CHIEF COMPLAINT: Persistent sadness and insomnia for 4 weeks\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Ms. Okonkwo presents with a 4-week history of persistent low mood, "
            "difficulty falling asleep, decreased appetite with 8-pound weight "
            "loss, and loss of interest in activities she previously enjoyed. She "
            "reports difficulty concentrating at work. She denies suicidal "
            "ideation or prior psychiatric history. Recent life stressor includes "
            "a relationship breakup 6 weeks ago.\n\n"
            "VITAL SIGNS:\n"
            "BP: 110/68 mmHg | HR: 64 bpm | Temp: 97.8°F | RR: 14 | SpO2: 99%\n\n"
            "ASSESSMENT: Major depressive episode\n"
            "PLAN: PHQ-9, TSH, start sertraline 50mg daily, "
            "therapy referral"
        ),
        "ground_truth": {
            "patient_name": "Linda Okonkwo",
            "age": 29,
            "sex": "Female",
            "chief_complaint": "Persistent sadness and insomnia for 4 weeks",
            "onset_date": "2024-08-17",
            "vital_signs": {
                "blood_pressure": "110/68",
                "heart_rate": 64,
                "temperature": 97.8,
                "respiratory_rate": 14,
                "spo2": 99,
            },
        },
    },
    {
        "id": "task1_note_008",
        "text": (
            "PATIENT: Michael Torres, 41 y/o Male\n"
            "DATE: 2024-10-01\n"
            "CHIEF COMPLAINT: Sudden onset right-sided flank pain for 6 hours\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Mr. Torres presents to the ED with sudden-onset severe right flank "
            "pain radiating to the groin that began 6 hours ago. Pain is colicky, "
            "rated 9/10, and associated with nausea and one episode of vomiting. "
            "He reports gross hematuria. He has a history of one prior kidney "
            "stone 3 years ago. He is otherwise healthy.\n\n"
            "VITAL SIGNS:\n"
            "BP: 148/92 mmHg | HR: 98 bpm | Temp: 99.1°F | RR: 20 | SpO2: 98%\n\n"
            "ASSESSMENT: Acute nephrolithiasis\n"
            "PLAN: CT abdomen/pelvis without contrast, IV fluids, "
            "ketorolac 30mg IV, ondansetron 4mg IV"
        ),
        "ground_truth": {
            "patient_name": "Michael Torres",
            "age": 41,
            "sex": "Male",
            "chief_complaint": "Sudden onset right-sided flank pain for 6 hours",
            "onset_date": "2024-10-01",
            "vital_signs": {
                "blood_pressure": "148/92",
                "heart_rate": 98,
                "temperature": 99.1,
                "respiratory_rate": 20,
                "spo2": 98,
            },
        },
    },
]

# ═══════════════════════════════════════════════════════════════
# TASK 2: Clinical Entity Extraction + Validation (Medium)
# Agent extracts: diagnoses+ICD-10, meds+dosages, detects conflicts
# ═══════════════════════════════════════════════════════════════

TASK_2_NOTES: list[dict[str, Any]] = [
    {
        "id": "task2_note_001",
        "text": (
            "PATIENT: Eleanor Grant, 68 y/o Female\n"
            "DATE: 2024-03-20\n"
            "ALLERGIES: Penicillin (anaphylaxis)\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Ms. Grant presents for follow-up of multiple chronic conditions. She "
            "has a 15-year history of type 2 diabetes, hypertension, and "
            "hyperlipidemia. Recently developed a urinary tract infection with "
            "dysuria and frequency.\n\n"
            "CURRENT MEDICATIONS:\n"
            "- Metformin 1000mg BID\n"
            "- Lisinopril 20mg daily\n"
            "- Atorvastatin 40mg daily\n"
            "- Amoxicillin 500mg TID (newly prescribed for UTI)\n\n"
            "ASSESSMENT:\n"
            "1. Type 2 diabetes mellitus - stable, HbA1c 7.2%\n"
            "2. Essential hypertension - controlled\n"
            "3. Hyperlipidemia - on statin therapy\n"
            "4. Urinary tract infection - acute\n\n"
            "VITAL SIGNS:\n"
            "BP: 136/84 mmHg | HR: 76 bpm | Temp: 99.8°F | RR: 16 | SpO2: 97%"
        ),
        "ground_truth": {
            "diagnoses": [
                {"condition": "diabetes_mellitus_type_2", "icd_code": "E11.9"},
                {"condition": "hypertension", "icd_code": "I10"},
                {"condition": "hyperlipidemia", "icd_code": "E78.5"},
                {"condition": "urinary_tract_infection", "icd_code": "N39.0"},
            ],
            "medications": [
                {"drug": "metformin", "dosage": "1000mg BID", "indication": "diabetes"},
                {"drug": "lisinopril", "dosage": "20mg daily", "indication": "hypertension"},
                {"drug": "atorvastatin", "dosage": "40mg daily", "indication": "hyperlipidemia"},
                {"drug": "amoxicillin", "dosage": "500mg TID", "indication": "UTI"},
            ],
            "allergies_mentioned": ["penicillin"],
            "inconsistencies": [
                {
                    "type": "drug_allergy_conflict",
                    "drug": "amoxicillin",
                    "allergy": "penicillin",
                    "severity": "high",
                    "description": "Amoxicillin prescribed despite documented penicillin allergy with anaphylaxis history.",
                },
            ],
        },
    },
    {
        "id": "task2_note_002",
        "text": (
            "PATIENT: Thomas Wright, 74 y/o Male\n"
            "DATE: 2024-04-15\n"
            "ALLERGIES: Aspirin (GI bleeding), Sulfa (rash)\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Mr. Wright presents with atrial fibrillation and heart failure "
            "managed on multiple medications. He also has COPD with a recent "
            "exacerbation and chronic kidney disease stage 3.\n\n"
            "CURRENT MEDICATIONS:\n"
            "- Warfarin 5mg daily (for AFib)\n"
            "- Ibuprofen 400mg TID (for arthritis pain)\n"
            "- Furosemide 40mg daily\n"
            "- Metoprolol 50mg BID\n"
            "- Trimethoprim-sulfamethoxazole DS BID (for bronchitis)\n"
            "- Albuterol inhaler PRN\n\n"
            "ASSESSMENT:\n"
            "1. Atrial fibrillation - rate controlled\n"
            "2. Heart failure with reduced EF (35%)\n"
            "3. COPD exacerbation - improving\n"
            "4. Chronic kidney disease stage 3b, eGFR 38\n"
            "5. Osteoarthritis - bilateral knees\n\n"
            "VITAL SIGNS:\n"
            "BP: 126/78 mmHg | HR: 72 bpm | Temp: 98.6°F | RR: 20 | SpO2: 94%"
        ),
        "ground_truth": {
            "diagnoses": [
                {"condition": "atrial_fibrillation", "icd_code": "I48.91"},
                {"condition": "heart_failure", "icd_code": "I50.9"},
                {"condition": "chronic_obstructive_pulmonary_disease", "icd_code": "J44.1"},
                {"condition": "chronic_kidney_disease", "icd_code": "N18.9"},
                {"condition": "osteoarthritis", "icd_code": "M19.90"},
            ],
            "medications": [
                {"drug": "warfarin", "dosage": "5mg daily", "indication": "atrial fibrillation"},
                {"drug": "ibuprofen", "dosage": "400mg TID", "indication": "arthritis"},
                {"drug": "furosemide", "dosage": "40mg daily", "indication": "heart failure"},
                {"drug": "metoprolol", "dosage": "50mg BID", "indication": "rate control"},
                {"drug": "trimethoprim-sulfamethoxazole", "dosage": "DS BID", "indication": "bronchitis"},
                {"drug": "albuterol", "dosage": "PRN", "indication": "COPD"},
            ],
            "allergies_mentioned": ["aspirin", "sulfa"],
            "inconsistencies": [
                {
                    "type": "drug_allergy_conflict",
                    "drug": "trimethoprim-sulfamethoxazole",
                    "allergy": "sulfa",
                    "severity": "high",
                    "description": "TMP-SMX prescribed despite documented sulfa allergy.",
                },
                {
                    "type": "drug_drug_interaction",
                    "drug_a": "warfarin",
                    "drug_b": "ibuprofen",
                    "severity": "high",
                    "description": "NSAID with anticoagulant significantly increases bleeding risk.",
                },
            ],
        },
    },
    {
        "id": "task2_note_003",
        "text": (
            "PATIENT: Priya Sharma, 55 y/o Female\n"
            "DATE: 2024-05-08\n"
            "ALLERGIES: No known drug allergies\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Ms. Sharma follows up for management of depression, type 2 diabetes, "
            "and chronic pain from lumbar stenosis. She reports increased back pain "
            "and requests stronger pain medication.\n\n"
            "CURRENT MEDICATIONS:\n"
            "- Sertraline 100mg daily\n"
            "- Metformin 850mg BID\n"
            "- Glipizide 10mg daily\n"
            "- Tramadol 50mg Q6H PRN\n"
            "- Gabapentin 300mg TID\n"
            "- Omeprazole 20mg daily\n\n"
            "ASSESSMENT:\n"
            "1. Major depressive disorder - partially controlled\n"
            "2. Type 2 diabetes - HbA1c 8.1%, above target\n"
            "3. Lumbar spinal stenosis with chronic pain\n"
            "4. GERD - stable on PPI\n\n"
            "VITAL SIGNS:\n"
            "BP: 132/80 mmHg | HR: 80 bpm | Temp: 98.6°F | RR: 16 | SpO2: 98%"
        ),
        "ground_truth": {
            "diagnoses": [
                {"condition": "major_depressive_disorder", "icd_code": "F33.0"},
                {"condition": "diabetes_mellitus_type_2", "icd_code": "E11.9"},
                {"condition": "chronic_pain_syndrome", "icd_code": "G89.29"},
                {"condition": "gastroesophageal_reflux_disease", "icd_code": "K21.0"},
            ],
            "medications": [
                {"drug": "sertraline", "dosage": "100mg daily", "indication": "depression"},
                {"drug": "metformin", "dosage": "850mg BID", "indication": "diabetes"},
                {"drug": "glipizide", "dosage": "10mg daily", "indication": "diabetes"},
                {"drug": "tramadol", "dosage": "50mg Q6H PRN", "indication": "pain"},
                {"drug": "gabapentin", "dosage": "300mg TID", "indication": "neuropathic pain"},
                {"drug": "omeprazole", "dosage": "20mg daily", "indication": "GERD"},
            ],
            "allergies_mentioned": [],
            "inconsistencies": [
                {
                    "type": "drug_drug_interaction",
                    "drug_a": "sertraline",
                    "drug_b": "tramadol",
                    "severity": "high",
                    "description": "SSRI + tramadol increases serotonin syndrome risk.",
                },
            ],
        },
    },
    {
        "id": "task2_note_004",
        "text": (
            "PATIENT: Marcus Johnson, 62 y/o Male\n"
            "DATE: 2024-06-12\n"
            "ALLERGIES: ACE inhibitors (angioedema)\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Mr. Johnson presents for routine follow-up of hypertension, coronary "
            "artery disease (s/p stent placement 2019), and benign prostatic "
            "hyperplasia. Blood pressure has been running high at home.\n\n"
            "CURRENT MEDICATIONS:\n"
            "- Enalapril 10mg BID\n"
            "- Aspirin 81mg daily\n"
            "- Clopidogrel 75mg daily\n"
            "- Omeprazole 20mg daily\n"
            "- Tamsulosin 0.4mg daily\n"
            "- Atorvastatin 80mg daily\n\n"
            "ASSESSMENT:\n"
            "1. Hypertension - uncontrolled, needs medication adjustment\n"
            "2. Coronary artery disease - stable, on dual antiplatelet\n"
            "3. BPH - stable symptoms\n"
            "4. Hyperlipidemia - on high-dose statin\n\n"
            "VITAL SIGNS:\n"
            "BP: 156/96 mmHg | HR: 68 bpm | Temp: 98.4°F | RR: 14 | SpO2: 98%"
        ),
        "ground_truth": {
            "diagnoses": [
                {"condition": "hypertension", "icd_code": "I10"},
                {"condition": "coronary_artery_disease", "icd_code": "I25.10"},
                {"condition": "benign_prostatic_hyperplasia", "icd_code": "N40.0"},
                {"condition": "hyperlipidemia", "icd_code": "E78.5"},
            ],
            "medications": [
                {"drug": "enalapril", "dosage": "10mg BID", "indication": "hypertension"},
                {"drug": "aspirin", "dosage": "81mg daily", "indication": "CAD"},
                {"drug": "clopidogrel", "dosage": "75mg daily", "indication": "CAD"},
                {"drug": "omeprazole", "dosage": "20mg daily", "indication": "GI protection"},
                {"drug": "tamsulosin", "dosage": "0.4mg daily", "indication": "BPH"},
                {"drug": "atorvastatin", "dosage": "80mg daily", "indication": "hyperlipidemia"},
            ],
            "allergies_mentioned": ["ace_inhibitors"],
            "inconsistencies": [
                {
                    "type": "drug_allergy_conflict",
                    "drug": "enalapril",
                    "allergy": "ace_inhibitors",
                    "severity": "high",
                    "description": "ACE inhibitor prescribed despite documented ACE inhibitor angioedema.",
                },
                {
                    "type": "drug_drug_interaction",
                    "drug_a": "clopidogrel",
                    "drug_b": "omeprazole",
                    "severity": "medium",
                    "description": "Omeprazole reduces clopidogrel activation via CYP2C19 inhibition.",
                },
            ],
        },
    },
    {
        "id": "task2_note_005",
        "text": (
            "PATIENT: Dorothy Evans, 80 y/o Female\n"
            "DATE: 2024-07-01\n"
            "ALLERGIES: Morphine (nausea/vomiting)\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Mrs. Evans presents with worsening knee pain and a new diagnosis of "
            "pneumonia. She has a history of osteoporosis with a prior vertebral "
            "compression fracture, hypertension, and hypothyroidism.\n\n"
            "CURRENT MEDICATIONS:\n"
            "- Amlodipine 10mg daily\n"
            "- Levothyroxine 75mcg daily\n"
            "- Alendronate 70mg weekly\n"
            "- Codeine 30mg Q6H PRN (newly prescribed for knee pain)\n"
            "- Azithromycin 500mg day 1, then 250mg x 4 days\n"
            "- Calcium/Vitamin D supplement daily\n\n"
            "ASSESSMENT:\n"
            "1. Community-acquired pneumonia\n"
            "2. Osteoarthritis - bilateral knees with acute flare\n"
            "3. Osteoporosis - on bisphosphonate\n"
            "4. Hypertension - controlled\n"
            "5. Hypothyroidism - stable on replacement\n\n"
            "VITAL SIGNS:\n"
            "BP: 140/78 mmHg | HR: 84 bpm | Temp: 100.8°F | RR: 22 | SpO2: 95%"
        ),
        "ground_truth": {
            "diagnoses": [
                {"condition": "pneumonia", "icd_code": "J18.9"},
                {"condition": "osteoarthritis", "icd_code": "M19.90"},
                {"condition": "osteoporosis", "icd_code": "M81.0"},
                {"condition": "hypertension", "icd_code": "I10"},
                {"condition": "hypothyroidism", "icd_code": "E03.9"},
            ],
            "medications": [
                {"drug": "amlodipine", "dosage": "10mg daily", "indication": "hypertension"},
                {"drug": "levothyroxine", "dosage": "75mcg daily", "indication": "hypothyroidism"},
                {"drug": "alendronate", "dosage": "70mg weekly", "indication": "osteoporosis"},
                {"drug": "codeine", "dosage": "30mg Q6H PRN", "indication": "pain"},
                {"drug": "azithromycin", "dosage": "500mg then 250mg x4", "indication": "pneumonia"},
                {"drug": "calcium/vitamin D", "dosage": "daily", "indication": "osteoporosis"},
            ],
            "allergies_mentioned": ["morphine"],
            "inconsistencies": [
                {
                    "type": "drug_allergy_conflict",
                    "drug": "codeine",
                    "allergy": "morphine",
                    "severity": "medium",
                    "description": "Codeine is metabolized to morphine. Cross-reactivity expected.",
                },
            ],
        },
    },
    {
        "id": "task2_note_006",
        "text": (
            "PATIENT: Ahmed Hassan, 49 y/o Male\n"
            "DATE: 2024-07-28\n"
            "ALLERGIES: No known drug allergies\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Mr. Hassan presents with poorly controlled type 2 diabetes and new "
            "fungal skin infection. He also has hypertension and an incidental "
            "finding of elevated liver enzymes on recent lab work.\n\n"
            "CURRENT MEDICATIONS:\n"
            "- Metformin 1000mg BID\n"
            "- Glipizide 10mg BID\n"
            "- Lisinopril 40mg daily\n"
            "- Fluconazole 200mg daily (new, for skin infection)\n"
            "- Aspirin 81mg daily\n\n"
            "ASSESSMENT:\n"
            "1. Type 2 diabetes - poorly controlled, HbA1c 9.5%\n"
            "2. Hypertension - controlled\n"
            "3. Cutaneous candidiasis\n"
            "4. Elevated transaminases - workup pending\n\n"
            "VITAL SIGNS:\n"
            "BP: 130/82 mmHg | HR: 78 bpm | Temp: 98.6°F | RR: 16 | SpO2: 99%"
        ),
        "ground_truth": {
            "diagnoses": [
                {"condition": "diabetes_mellitus_type_2", "icd_code": "E11.9"},
                {"condition": "hypertension", "icd_code": "I10"},
            ],
            "medications": [
                {"drug": "metformin", "dosage": "1000mg BID", "indication": "diabetes"},
                {"drug": "glipizide", "dosage": "10mg BID", "indication": "diabetes"},
                {"drug": "lisinopril", "dosage": "40mg daily", "indication": "hypertension"},
                {"drug": "fluconazole", "dosage": "200mg daily", "indication": "fungal infection"},
                {"drug": "aspirin", "dosage": "81mg daily", "indication": "cardiovascular prevention"},
            ],
            "allergies_mentioned": [],
            "inconsistencies": [
                {
                    "type": "drug_drug_interaction",
                    "drug_a": "glipizide",
                    "drug_b": "fluconazole",
                    "severity": "high",
                    "description": "Fluconazole inhibits CYP2C9, increasing glipizide levels and severe hypoglycemia risk.",
                },
            ],
        },
    },
    {
        "id": "task2_note_007",
        "text": (
            "PATIENT: Catherine Brooks, 72 y/o Female\n"
            "DATE: 2024-08-14\n"
            "ALLERGIES: Aspirin (GI upset), Contrast dye (hives)\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Ms. Brooks has a history of atrial fibrillation, diabetes, and "
            "rheumatoid arthritis. Presents today for pre-procedure evaluation "
            "before a CT angiogram with contrast. Also reporting increased "
            "joint inflammation.\n\n"
            "CURRENT MEDICATIONS:\n"
            "- Warfarin 3mg daily\n"
            "- Metformin 500mg BID\n"
            "- Naproxen 500mg BID (for RA flare)\n"
            "- Methotrexate 15mg weekly\n"
            "- Folic acid 1mg daily\n"
            "- Pantoprazole 40mg daily\n\n"
            "PROCEDURE PLANNED: CT angiogram with iodinated contrast\n\n"
            "ASSESSMENT:\n"
            "1. Atrial fibrillation on anticoagulation\n"
            "2. Type 2 diabetes on metformin\n"
            "3. Rheumatoid arthritis - active flare\n"
            "4. Contrast dye allergy - needs premedication protocol\n\n"
            "VITAL SIGNS:\n"
            "BP: 138/86 mmHg | HR: 74 bpm irreg | Temp: 98.2°F | RR: 16 | SpO2: 97%"
        ),
        "ground_truth": {
            "diagnoses": [
                {"condition": "atrial_fibrillation", "icd_code": "I48.91"},
                {"condition": "diabetes_mellitus_type_2", "icd_code": "E11.9"},
                {"condition": "rheumatoid_arthritis", "icd_code": "M06.9"},
            ],
            "medications": [
                {"drug": "warfarin", "dosage": "3mg daily", "indication": "atrial fibrillation"},
                {"drug": "metformin", "dosage": "500mg BID", "indication": "diabetes"},
                {"drug": "naproxen", "dosage": "500mg BID", "indication": "RA"},
                {"drug": "methotrexate", "dosage": "15mg weekly", "indication": "RA"},
                {"drug": "folic acid", "dosage": "1mg daily", "indication": "methotrexate support"},
                {"drug": "pantoprazole", "dosage": "40mg daily", "indication": "GI protection"},
            ],
            "allergies_mentioned": ["aspirin", "contrast_dye"],
            "inconsistencies": [
                {
                    "type": "drug_allergy_conflict",
                    "drug": "naproxen",
                    "allergy": "aspirin",
                    "severity": "medium",
                    "description": "NSAID prescribed despite aspirin allergy (cross-sensitivity).",
                },
                {
                    "type": "drug_allergy_conflict",
                    "drug": "iodinated_contrast",
                    "allergy": "contrast_dye",
                    "severity": "high",
                    "description": "CT with contrast planned despite contrast dye allergy history.",
                },
                {
                    "type": "drug_drug_interaction",
                    "drug_a": "metformin",
                    "drug_b": "iodinated_contrast",
                    "severity": "high",
                    "description": "Metformin must be held 48h before/after contrast for lactic acidosis risk.",
                },
            ],
        },
    },
    {
        "id": "task2_note_008",
        "text": (
            "PATIENT: William Foster, 56 y/o Male\n"
            "DATE: 2024-09-05\n"
            "ALLERGIES: Penicillin (rash)\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Mr. Foster presents with new-onset seizures and a known history of "
            "bipolar disorder, hypertension, and sleep apnea. He was recently "
            "started on an antibiotic for a skin infection.\n\n"
            "CURRENT MEDICATIONS:\n"
            "- Lithium 600mg BID\n"
            "- Amlodipine 5mg daily\n"
            "- CPAP therapy nightly\n"
            "- Cephalexin 500mg QID (for cellulitis)\n"
            "- Levetiracetam 500mg BID (newly started for seizures)\n\n"
            "ASSESSMENT:\n"
            "1. New-onset seizure disorder - workup in progress\n"
            "2. Bipolar disorder - stable on lithium\n"
            "3. Hypertension - controlled\n"
            "4. Sleep apnea - compliant with CPAP\n"
            "5. Cellulitis, left lower extremity\n\n"
            "VITAL SIGNS:\n"
            "BP: 128/78 mmHg | HR: 72 bpm | Temp: 99.4°F | RR: 16 | SpO2: 97%"
        ),
        "ground_truth": {
            "diagnoses": [
                {"condition": "seizure_disorder", "icd_code": "G40.909"},
                {"condition": "bipolar_disorder", "icd_code": "F31.9"},
                {"condition": "hypertension", "icd_code": "I10"},
                {"condition": "sleep_apnea", "icd_code": "G47.33"},
                {"condition": "cellulitis", "icd_code": "L03.90"},
            ],
            "medications": [
                {"drug": "lithium", "dosage": "600mg BID", "indication": "bipolar disorder"},
                {"drug": "amlodipine", "dosage": "5mg daily", "indication": "hypertension"},
                {"drug": "cephalexin", "dosage": "500mg QID", "indication": "cellulitis"},
                {"drug": "levetiracetam", "dosage": "500mg BID", "indication": "seizures"},
            ],
            "allergies_mentioned": ["penicillin"],
            "inconsistencies": [
                {
                    "type": "drug_allergy_conflict",
                    "drug": "cephalexin",
                    "allergy": "penicillin",
                    "severity": "medium",
                    "description": "Cephalosporin prescribed with penicillin allergy. Low cross-reactivity but needs documentation.",
                },
            ],
        },
    },
]


# ═══════════════════════════════════════════════════════════════
# TASK 3: Risk Assessment + Clinical Reasoning (Hard)
# Agent assesses: risk level, critical flags, readmission risk, summary
# ═══════════════════════════════════════════════════════════════

TASK_3_NOTES: list[dict[str, Any]] = [
    {
        "id": "task3_note_001",
        "text": (
            "PATIENT: George Martinez, 78 y/o Male\n"
            "DATE: 2024-03-25\n"
            "ALLERGIES: Penicillin\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Mr. Martinez is a 78-year-old male admitted for acute decompensated "
            "heart failure. He has a history of ischemic cardiomyopathy with EF 25%, "
            "recent MI 3 months ago, type 2 diabetes, CKD stage 4 (eGFR 22), and "
            "atrial fibrillation on warfarin. He presents with worsening dyspnea, "
            "orthopnea, and 15-pound weight gain over 2 weeks. BNP elevated at 1850.\n\n"
            "He was seen in the ED twice in the past 30 days for similar symptoms.\n\n"
            "CURRENT MEDICATIONS:\n"
            "- Warfarin 4mg daily | Carvedilol 12.5mg BID | Furosemide 80mg BID\n"
            "- Lisinopril 5mg daily | Aspirin 81mg daily | Atorvastatin 40mg\n"
            "- Metformin 500mg BID | Insulin glargine 20 units nightly\n\n"
            "VITAL SIGNS:\n"
            "BP: 98/62 mmHg | HR: 110 bpm irreg | Temp: 98.2°F | RR: 28 | SpO2: 89%\n\n"
            "LABS: BNP 1850, Cr 3.2 (baseline 2.1), K+ 5.8, INR 3.8\n\n"
            "ASSESSMENT:\n"
            "1. Acute decompensated heart failure\n"
            "2. Acute on chronic kidney injury\n"
            "3. Hyperkalemia\n"
            "4. Supratherapeutic INR\n"
            "5. Type 2 diabetes\n"
            "6. Atrial fibrillation with RVR"
        ),
        "ground_truth": {
            "risk_level": "high",
            "risk_factors": [
                "EF 25%", "recent MI within 3 months", "CKD stage 4",
                "age over 75", "multiple ED visits in 30 days",
                "acute kidney injury", "hyperkalemia", "supratherapeutic INR",
                "hypotension", "tachycardia", "hypoxia",
            ],
            "critical_flags": [
                {"flag": "Hyperkalemia K+ 5.8", "action": "Urgent treatment with calcium gluconate, insulin/glucose, kayexalate", "urgency": "immediate"},
                {"flag": "Supratherapeutic INR 3.8 on warfarin+aspirin", "action": "Hold warfarin, consider vitamin K, bleeding risk assessment", "urgency": "immediate"},
                {"flag": "Hypoxia SpO2 89%", "action": "Supplemental oxygen, consider BiPAP, monitor respiratory status", "urgency": "immediate"},
                {"flag": "Metformin with eGFR 22", "action": "Hold metformin - contraindicated with eGFR < 30, lactic acidosis risk", "urgency": "urgent"},
            ],
            "readmission_risk_score": 0.88,
            "clinical_summary": (
                "High-risk 78-year-old male with acute decompensated heart failure "
                "on background of severe ischemic cardiomyopathy (EF 25%), recent MI, "
                "and CKD stage 4. Multiple immediate concerns include hyperkalemia "
                "(K+ 5.8), supratherapeutic anticoagulation (INR 3.8), and hypoxia. "
                "Dual anticoagulation with warfarin and aspirin increases bleeding risk. "
                "Metformin is contraindicated at current renal function. High readmission "
                "risk given 2 ED visits in 30 days and multiple decompensated conditions."
            ),
        },
    },
    {
        "id": "task3_note_002",
        "text": (
            "PATIENT: Susan Baker, 65 y/o Female\n"
            "DATE: 2024-04-18\n"
            "ALLERGIES: None\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Ms. Baker presents with new-onset confusion and fall at home. She has "
            "a history of type 2 diabetes, hypertension, and recently started "
            "antibiotics for a urinary tract infection 3 days ago. Daughter reports "
            "she has been more drowsy and confused over the past 24 hours.\n\n"
            "CURRENT MEDICATIONS:\n"
            "- Metformin 1000mg BID | Glipizide 10mg daily\n"
            "- Lisinopril 20mg daily | Amlodipine 5mg daily\n"
            "- Ciprofloxacin 500mg BID (started 3 days ago for UTI)\n\n"
            "VITAL SIGNS:\n"
            "BP: 102/58 mmHg | HR: 96 bpm | Temp: 101.8°F | RR: 22 | SpO2: 95%\n\n"
            "LABS: WBC 18.2, Glucose 52, Cr 1.8 (baseline 1.0), Lactate 3.1\n\n"
            "ASSESSMENT:\n"
            "1. Altered mental status - likely multifactorial\n"
            "2. Severe hypoglycemia\n"
            "3. Urosepsis\n"
            "4. Acute kidney injury\n"
            "5. Fall - no acute fracture on imaging"
        ),
        "ground_truth": {
            "risk_level": "high",
            "risk_factors": [
                "age 65", "altered mental status", "severe hypoglycemia",
                "sepsis with elevated lactate", "acute kidney injury",
                "fall risk", "fever", "hypotension",
            ],
            "critical_flags": [
                {"flag": "Severe hypoglycemia glucose 52", "action": "Immediate IV dextrose, hold glipizide, frequent glucose monitoring", "urgency": "immediate"},
                {"flag": "Sepsis with lactate 3.1", "action": "IV antibiotics, fluid resuscitation, monitor for septic shock", "urgency": "immediate"},
                {"flag": "Acute kidney injury Cr 1.8 from 1.0", "action": "IV fluids, hold metformin, monitor urine output and renal function", "urgency": "urgent"},
            ],
            "readmission_risk_score": 0.72,
            "clinical_summary": (
                "65-year-old female presenting with altered mental status and fall "
                "in the setting of urosepsis and severe hypoglycemia. The hypoglycemia "
                "is likely multifactorial: glipizide use combined with reduced oral intake "
                "and acute kidney injury reducing drug clearance. Elevated lactate suggests "
                "early sepsis requiring aggressive fluid resuscitation and broad-spectrum "
                "antibiotics. Metformin should be held given AKI. Fall risk assessment "
                "and close monitoring needed."
            ),
        },
    },
    {
        "id": "task3_note_003",
        "text": (
            "PATIENT: Richard Lee, 70 y/o Male\n"
            "DATE: 2024-05-22\n"
            "ALLERGIES: Sulfa drugs\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Mr. Lee is a 70-year-old male with COPD (on home O2 2L), coronary artery "
            "disease, and depression presenting with worsening shortness of breath and "
            "productive cough with yellow sputum for 5 days. He has had 3 COPD "
            "exacerbations requiring hospitalization in the past year.\n\n"
            "CURRENT MEDICATIONS:\n"
            "- Tiotropium 18mcg daily | Fluticasone/salmeterol 250/50 BID\n"
            "- Albuterol nebulizer Q4H | Prednisone 40mg daily (started 3 days ago)\n"
            "- Aspirin 81mg daily | Metoprolol 25mg BID | Atorvastatin 20mg daily\n"
            "- Sertraline 50mg daily\n\n"
            "VITAL SIGNS:\n"
            "BP: 144/88 mmHg | HR: 104 bpm | Temp: 100.4°F | RR: 26 | SpO2: 88% on 2L\n\n"
            "LABS: WBC 14.8, ABG: pH 7.32, pCO2 52, pO2 58\n\n"
            "ASSESSMENT:\n"
            "1. Acute COPD exacerbation with possible pneumonia\n"
            "2. Acute hypercapnic respiratory failure\n"
            "3. CAD - stable\n"
            "4. Depression"
        ),
        "ground_truth": {
            "risk_level": "high",
            "risk_factors": [
                "age 70", "COPD on home oxygen", "3 hospitalizations past year",
                "hypercapnic respiratory failure", "hypoxia on supplemental O2",
                "tachycardia", "tachypnea", "fever suggesting infection",
            ],
            "critical_flags": [
                {"flag": "Hypercapnic respiratory failure pCO2 52", "action": "Consider BiPAP/NIV, monitor ABGs closely, ICU evaluation", "urgency": "immediate"},
                {"flag": "Hypoxia SpO2 88% on 2L baseline O2", "action": "Increase O2 delivery, titrate carefully to avoid CO2 retention", "urgency": "immediate"},
                {"flag": "Frequent exacerbations 3 in past year", "action": "Pulmonology consult, escalate maintenance therapy, home care evaluation", "urgency": "urgent"},
            ],
            "readmission_risk_score": 0.82,
            "clinical_summary": (
                "70-year-old male with severe COPD on home oxygen presenting with acute "
                "exacerbation complicated by hypercapnic respiratory failure. History of "
                "3 hospitalizations in the past year indicates poorly controlled disease. "
                "Current ABG shows respiratory acidosis with CO2 retention. Fever and "
                "productive cough suggest superimposed pneumonia. Needs BiPAP evaluation, "
                "antibiotics for possible pneumonia, continued systemic steroids, and "
                "pulmonology consultation for long-term management optimization."
            ),
        },
    },
    {
        "id": "task3_note_004",
        "text": (
            "PATIENT: Angela White, 55 y/o Female\n"
            "DATE: 2024-06-30\n"
            "ALLERGIES: None\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Ms. White presents for routine diabetes follow-up. She has well-controlled "
            "type 2 diabetes, mild hypertension, and hypothyroidism. She reports feeling "
            "well with no complaints. She exercises regularly and follows a healthy diet.\n\n"
            "CURRENT MEDICATIONS:\n"
            "- Metformin 500mg BID | Lisinopril 10mg daily\n"
            "- Levothyroxine 50mcg daily\n\n"
            "VITAL SIGNS:\n"
            "BP: 124/78 mmHg | HR: 72 bpm | Temp: 98.6°F | RR: 14 | SpO2: 99%\n\n"
            "LABS: HbA1c 6.4%, Cr 0.9, TSH 2.1, lipid panel normal\n\n"
            "ASSESSMENT:\n"
            "1. Type 2 diabetes - well controlled\n"
            "2. Hypertension - at goal\n"
            "3. Hypothyroidism - euthyroid on replacement"
        ),
        "ground_truth": {
            "risk_level": "low",
            "risk_factors": [
                "type 2 diabetes (well controlled)",
                "hypertension (at goal)",
            ],
            "critical_flags": [],
            "readmission_risk_score": 0.08,
            "clinical_summary": (
                "55-year-old female with well-controlled chronic conditions. HbA1c at "
                "goal, blood pressure controlled, thyroid function normal. No acute "
                "issues identified. Continue current management with routine follow-up."
            ),
        },
    },
    {
        "id": "task3_note_005",
        "text": (
            "PATIENT: Frank Robinson, 82 y/o Male\n"
            "DATE: 2024-07-15\n"
            "ALLERGIES: Penicillin, Codeine\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Mr. Robinson is an 82-year-old nursing home resident with advanced dementia, "
            "recurrent aspiration pneumonia, heart failure (EF 30%), and diabetes. He is "
            "admitted for the third time in 60 days with aspiration pneumonia. Family is "
            "considering comfort care. He has a stage 3 pressure ulcer on his sacrum.\n\n"
            "CURRENT MEDICATIONS:\n"
            "- Donepezil 10mg daily | Furosemide 60mg daily\n"
            "- Carvedilol 6.25mg BID | Insulin sliding scale\n"
            "- Vancomycin 1g Q12H | Piperacillin-tazobactam 3.375g Q6H\n\n"
            "VITAL SIGNS:\n"
            "BP: 88/52 mmHg | HR: 108 bpm | Temp: 102.2°F | RR: 30 | SpO2: 86%\n\n"
            "LABS: WBC 22.4, Cr 2.6, Lactate 4.2, Albumin 2.0, procalcitonin 8.5\n\n"
            "ASSESSMENT:\n"
            "1. Recurrent aspiration pneumonia - third episode\n"
            "2. Sepsis\n"
            "3. Heart failure - decompensated\n"
            "4. Advanced dementia\n"
            "5. Pressure injury stage 3\n"
            "6. Malnutrition"
        ),
        "ground_truth": {
            "risk_level": "high",
            "risk_factors": [
                "age 82", "advanced dementia", "recurrent aspiration pneumonia",
                "3 admissions in 60 days", "nursing home resident", "sepsis",
                "severe hypotension", "hypoxia", "malnutrition albumin 2.0",
                "pressure ulcer stage 3", "heart failure EF 30%",
            ],
            "critical_flags": [
                {"flag": "Sepsis with lactate 4.2", "action": "Aggressive fluid resuscitation, vasopressors if unresponsive, ICU evaluation", "urgency": "immediate"},
                {"flag": "Severe hypoxia SpO2 86%", "action": "High-flow oxygen, consider intubation vs goals of care discussion", "urgency": "immediate"},
                {"flag": "Hypotension BP 88/52 with tachycardia", "action": "Fluid bolus, vasopressors, hold carvedilol", "urgency": "immediate"},
                {"flag": "Goals of care discussion needed", "action": "Family meeting for advance directive review, palliative care consult", "urgency": "urgent"},
            ],
            "readmission_risk_score": 0.95,
            "clinical_summary": (
                "82-year-old nursing home resident with advanced dementia presenting with "
                "third aspiration pneumonia in 60 days, now complicated by sepsis with "
                "hemodynamic instability. Multiple markers of poor prognosis: severe sepsis "
                "(lactate 4.2), malnutrition (albumin 2.0), decompensated heart failure, "
                "and non-healing pressure ulcer. Goals of care discussion with family is "
                "critical given recurrent nature of admissions and overall trajectory. "
                "Palliative care consultation recommended."
            ),
        },
    },
    {
        "id": "task3_note_006",
        "text": (
            "PATIENT: Nancy Cooper, 60 y/o Female\n"
            "DATE: 2024-08-20\n"
            "ALLERGIES: None\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Ms. Cooper presents with a 2-week history of progressive bilateral leg "
            "swelling and fatigue. She has a history of cirrhosis secondary to NASH, "
            "type 2 diabetes, and obesity. Recent ultrasound shows new ascites. "
            "She reports mild confusion that her husband has noticed over the past few days.\n\n"
            "CURRENT MEDICATIONS:\n"
            "- Furosemide 40mg daily | Spironolactone 100mg daily\n"
            "- Metformin 1000mg BID | Lactulose 30mL TID\n"
            "- Propranolol 20mg BID | Rifaximin 550mg BID\n\n"
            "VITAL SIGNS:\n"
            "BP: 106/64 mmHg | HR: 82 bpm | Temp: 98.8°F | RR: 18 | SpO2: 96%\n\n"
            "LABS: Na 128, Cr 1.6, Albumin 2.4, INR 1.8, Ammonia 95, MELD 22\n\n"
            "ASSESSMENT:\n"
            "1. Decompensated cirrhosis with new ascites\n"
            "2. Hepatic encephalopathy grade 2\n"
            "3. Hyponatremia\n"
            "4. Type 2 diabetes\n"
            "5. Obesity"
        ),
        "ground_truth": {
            "risk_level": "high",
            "risk_factors": [
                "decompensated cirrhosis", "MELD score 22", "hepatic encephalopathy",
                "new ascites", "hyponatremia Na 128", "coagulopathy INR 1.8",
                "malnutrition albumin 2.4", "AKI Cr 1.6",
            ],
            "critical_flags": [
                {"flag": "Hepatic encephalopathy grade 2 with confusion", "action": "Optimize lactulose, ensure rifaximin dosing, identify and treat precipitant", "urgency": "urgent"},
                {"flag": "Hyponatremia Na 128", "action": "Fluid restriction, monitor sodium closely, avoid rapid correction", "urgency": "urgent"},
                {"flag": "MELD 22 with decompensation", "action": "Hepatology referral, liver transplant evaluation if appropriate", "urgency": "urgent"},
            ],
            "readmission_risk_score": 0.78,
            "clinical_summary": (
                "60-year-old female with decompensated NASH cirrhosis (MELD 22) presenting "
                "with new ascites and grade 2 hepatic encephalopathy. Multiple markers of "
                "hepatic decompensation including hyponatremia, coagulopathy, and hypoalbuminemia. "
                "Current management with lactulose and rifaximin for encephalopathy. Needs "
                "hepatology input for transplant evaluation and optimization of diuretic therapy. "
                "Metformin should be used cautiously given liver disease and AKI."
            ),
        },
    },
    {
        "id": "task3_note_007",
        "text": (
            "PATIENT: Kevin Anderson, 48 y/o Male\n"
            "DATE: 2024-09-10\n"
            "ALLERGIES: None\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Mr. Anderson presents with crushing substernal chest pain radiating to "
            "the left arm for 2 hours. ECG shows ST elevation in leads II, III, aVF. "
            "He has no prior cardiac history but has a 30 pack-year smoking history, "
            "untreated hypertension, and family history of MI (father at age 50).\n\n"
            "CURRENT MEDICATIONS:\n"
            "- None (no regular medications)\n\n"
            "VITAL SIGNS:\n"
            "BP: 168/102 mmHg | HR: 112 bpm | Temp: 98.6°F | RR: 22 | SpO2: 96%\n\n"
            "LABS: Troponin I 15.2 (normal < 0.04), CK-MB 85\n\n"
            "ASSESSMENT:\n"
            "1. Acute STEMI - inferior wall\n"
            "2. Undiagnosed hypertension\n"
            "3. Active tobacco use"
        ),
        "ground_truth": {
            "risk_level": "high",
            "risk_factors": [
                "acute STEMI", "significantly elevated troponin",
                "30 pack-year smoking history", "untreated hypertension",
                "family history of premature MI", "tachycardia",
            ],
            "critical_flags": [
                {"flag": "Acute STEMI with ST elevation", "action": "Emergent cardiac catheterization, activate cath lab, door-to-balloon time < 90 min", "urgency": "immediate"},
                {"flag": "Troponin I 15.2 (380x normal)", "action": "Antiplatelet therapy (aspirin + P2Y12 inhibitor), heparin, prepare for PCI", "urgency": "immediate"},
            ],
            "readmission_risk_score": 0.45,
            "clinical_summary": (
                "48-year-old male presenting with acute inferior STEMI requiring emergent "
                "cardiac catheterization. Major cardiovascular risk factors include 30 pack-year "
                "smoking history, untreated hypertension, and family history of premature MI. "
                "Markedly elevated troponin indicates significant myocardial damage. Needs "
                "emergent PCI, dual antiplatelet therapy, and comprehensive cardiovascular "
                "risk factor management post-intervention including smoking cessation."
            ),
        },
    },
    {
        "id": "task3_note_008",
        "text": (
            "PATIENT: Patricia Young, 42 y/o Female\n"
            "DATE: 2024-10-05\n"
            "ALLERGIES: None\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "Ms. Young presents for follow-up of mild asthma and seasonal allergies. "
            "She uses her rescue inhaler about once weekly and has had no exacerbations "
            "in over a year. She also has mild intermittent anxiety managed with "
            "relaxation techniques. No hospitalizations in the past 5 years.\n\n"
            "CURRENT MEDICATIONS:\n"
            "- Albuterol inhaler PRN | Fluticasone nasal spray daily\n"
            "- Cetirizine 10mg daily\n\n"
            "VITAL SIGNS:\n"
            "BP: 116/72 mmHg | HR: 68 bpm | Temp: 98.4°F | RR: 14 | SpO2: 99%\n\n"
            "ASSESSMENT:\n"
            "1. Mild persistent asthma - well controlled\n"
            "2. Allergic rhinitis\n"
            "3. Mild intermittent anxiety"
        ),
        "ground_truth": {
            "risk_level": "low",
            "risk_factors": [
                "mild asthma (well controlled)",
            ],
            "critical_flags": [],
            "readmission_risk_score": 0.05,
            "clinical_summary": (
                "42-year-old female with well-controlled mild asthma and seasonal allergies. "
                "No exacerbations in over a year, minimal rescue inhaler use. Anxiety managed "
                "non-pharmacologically. No acute concerns. Continue current management."
            ),
        },
    },
]


# ─── Master lookup ───
NOTES_BY_TASK: dict[str, list[dict[str, Any]]] = {
    "task_1": TASK_1_NOTES,
    "task_2": TASK_2_NOTES,
    "task_3": TASK_3_NOTES,
}
