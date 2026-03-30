"""
Medical Ontology — ICD-10 codes, SNOMED synonyms, and condition mappings.

Provides deterministic medical term matching for the grading system.
~50 common conditions with abbreviations/synonyms and ICD-10 codes.
"""

# ─────────────────────────────────────────────────────────────────
# SYNONYM_MAP: canonical_name → [abbreviations, alternate names]
# Used by graders to accept equivalent medical terminology.
# ─────────────────────────────────────────────────────────────────

SYNONYM_MAP: dict[str, list[str]] = {
    # Cardiovascular
    "hypertension": [
        "htn", "high blood pressure", "elevated bp", "elevated blood pressure",
        "hypertensive disease", "arterial hypertension",
    ],
    "hypotension": [
        "low blood pressure", "low bp",
    ],
    "atrial_fibrillation": [
        "afib", "a-fib", "af", "atrial fib", "auricular fibrillation",
    ],
    "heart_failure": [
        "hf", "chf", "congestive heart failure", "cardiac failure",
        "heart failure with reduced ejection fraction", "hfref",
        "heart failure with preserved ejection fraction", "hfpef",
    ],
    "coronary_artery_disease": [
        "cad", "coronary heart disease", "chd", "ischemic heart disease",
        "ihd", "atherosclerotic heart disease", "ashd",
    ],
    "myocardial_infarction": [
        "mi", "heart attack", "ami", "acute mi", "stemi", "nstemi",
        "st elevation mi", "non-st elevation mi",
    ],
    "deep_vein_thrombosis": [
        "dvt", "venous thrombosis", "deep venous thrombosis",
    ],
    "pulmonary_embolism": [
        "pe", "pulmonary thromboembolism",
    ],
    "peripheral_artery_disease": [
        "pad", "peripheral vascular disease", "pvd",
    ],
    "hyperlipidemia": [
        "high cholesterol", "dyslipidemia", "elevated lipids",
        "hypercholesterolemia", "hld",
    ],

    # Endocrine
    "diabetes_mellitus_type_2": [
        "dm2", "t2dm", "type 2 diabetes", "type ii diabetes", "niddm",
        "adult-onset diabetes", "dm type 2", "diabetes type 2",
    ],
    "diabetes_mellitus_type_1": [
        "dm1", "t1dm", "type 1 diabetes", "type i diabetes", "iddm",
        "juvenile diabetes", "dm type 1",
    ],
    "hypothyroidism": [
        "underactive thyroid", "low thyroid", "hashimotos",
        "hashimoto's thyroiditis",
    ],
    "hyperthyroidism": [
        "overactive thyroid", "graves disease", "thyrotoxicosis",
    ],
    "obesity": [
        "morbid obesity", "bmi over 30", "obese",
    ],

    # Respiratory
    "chronic_obstructive_pulmonary_disease": [
        "copd", "chronic bronchitis", "emphysema",
        "chronic obstructive lung disease", "cold",
    ],
    "asthma": [
        "bronchial asthma", "reactive airway disease", "rad",
    ],
    "pneumonia": [
        "pna", "lung infection", "community acquired pneumonia", "cap",
        "hospital acquired pneumonia", "hap",
    ],
    "pulmonary_fibrosis": [
        "ipf", "idiopathic pulmonary fibrosis", "lung fibrosis",
    ],

    # Neurological
    "cerebrovascular_accident": [
        "cva", "stroke", "ischemic stroke", "hemorrhagic stroke",
        "brain attack", "cerebral infarction",
    ],
    "transient_ischemic_attack": [
        "tia", "mini stroke", "mini-stroke",
    ],
    "seizure_disorder": [
        "epilepsy", "seizures", "convulsive disorder",
    ],
    "dementia": [
        "alzheimers", "alzheimer's disease", "cognitive decline",
        "neurocognitive disorder", "senile dementia",
    ],
    "migraine": [
        "migraine headache", "migraine with aura", "migraine without aura",
    ],
    "tension_headache": [
        "tension-type headache", "tth", "stress headache", "muscle contraction headache",
    ],

    # Renal
    "chronic_kidney_disease": [
        "ckd", "chronic renal failure", "crf", "chronic renal insufficiency",
        "renal disease",
    ],
    "acute_kidney_injury": [
        "aki", "acute renal failure", "arf",
    ],
    "end_stage_renal_disease": [
        "esrd", "end stage kidney disease", "eskd",
    ],

    # Gastrointestinal
    "gastroesophageal_reflux_disease": [
        "gerd", "acid reflux", "reflux", "heartburn",
    ],
    "peptic_ulcer_disease": [
        "pud", "gastric ulcer", "duodenal ulcer", "stomach ulcer",
    ],
    "inflammatory_bowel_disease": [
        "ibd", "crohns disease", "crohn's", "ulcerative colitis", "uc",
    ],
    "cirrhosis": [
        "liver cirrhosis", "hepatic cirrhosis", "end stage liver disease",
    ],

    # Musculoskeletal
    "osteoarthritis": [
        "oa", "degenerative joint disease", "djd", "wear and tear arthritis",
    ],
    "rheumatoid_arthritis": [
        "ra", "rheumatoid disease",
    ],
    "osteoporosis": [
        "bone loss", "decreased bone density", "low bone mass",
    ],
    "fracture": [
        "fx", "broken bone", "bone fracture",
    ],

    # Mental Health
    "major_depressive_disorder": [
        "mdd", "depression", "clinical depression", "major depression",
        "depressive disorder",
    ],
    "generalized_anxiety_disorder": [
        "gad", "anxiety", "anxiety disorder", "chronic anxiety",
    ],
    "bipolar_disorder": [
        "bipolar", "manic depressive", "bipolar affective disorder",
    ],
    "post_traumatic_stress_disorder": [
        "ptsd", "post-traumatic stress", "trauma disorder",
    ],

    # Infectious
    "urinary_tract_infection": [
        "uti", "bladder infection", "cystitis",
    ],
    "cellulitis": [
        "skin infection", "soft tissue infection",
    ],
    "sepsis": [
        "septicemia", "blood infection", "systemic infection",
        "severe sepsis", "septic shock",
    ],

    # Other
    "anemia": [
        "low hemoglobin", "low hgb", "iron deficiency anemia", "ida",
    ],
    "benign_prostatic_hyperplasia": [
        "bph", "enlarged prostate", "prostatic hypertrophy",
    ],
    "chronic_pain_syndrome": [
        "chronic pain", "persistent pain",
    ],
    "sleep_apnea": [
        "osa", "obstructive sleep apnea", "sleep disordered breathing",
    ],
}

# ─────────────────────────────────────────────────────────────────
# ICD-10 CODES: canonical_name → ICD-10-CM code
# ─────────────────────────────────────────────────────────────────

ICD10_CODES: dict[str, str] = {
    # Cardiovascular
    "hypertension": "I10",
    "hypotension": "I95.9",
    "atrial_fibrillation": "I48.91",
    "heart_failure": "I50.9",
    "coronary_artery_disease": "I25.10",
    "myocardial_infarction": "I21.9",
    "deep_vein_thrombosis": "I82.90",
    "pulmonary_embolism": "I26.99",
    "peripheral_artery_disease": "I73.9",
    "hyperlipidemia": "E78.5",

    # Endocrine
    "diabetes_mellitus_type_2": "E11.9",
    "diabetes_mellitus_type_1": "E10.9",
    "hypothyroidism": "E03.9",
    "hyperthyroidism": "E05.90",
    "obesity": "E66.9",

    # Respiratory
    "chronic_obstructive_pulmonary_disease": "J44.1",
    "asthma": "J45.909",
    "pneumonia": "J18.9",
    "pulmonary_fibrosis": "J84.10",

    # Neurological
    "cerebrovascular_accident": "I63.9",
    "transient_ischemic_attack": "G45.9",
    "seizure_disorder": "G40.909",
    "dementia": "F03.90",
    "migraine": "G43.909",
    "tension_headache": "G44.209",

    # Renal
    "chronic_kidney_disease": "N18.9",
    "acute_kidney_injury": "N17.9",
    "end_stage_renal_disease": "N18.6",

    # Gastrointestinal
    "gastroesophageal_reflux_disease": "K21.0",
    "peptic_ulcer_disease": "K27.9",
    "inflammatory_bowel_disease": "K52.9",
    "cirrhosis": "K74.60",

    # Musculoskeletal
    "osteoarthritis": "M19.90",
    "rheumatoid_arthritis": "M06.9",
    "osteoporosis": "M81.0",
    "fracture": "T14.8",

    # Mental Health
    "major_depressive_disorder": "F33.0",
    "generalized_anxiety_disorder": "F41.1",
    "bipolar_disorder": "F31.9",
    "post_traumatic_stress_disorder": "F43.10",

    # Infectious
    "urinary_tract_infection": "N39.0",
    "cellulitis": "L03.90",
    "sepsis": "A41.9",

    # Other
    "anemia": "D64.9",
    "benign_prostatic_hyperplasia": "N40.0",
    "chronic_pain_syndrome": "G89.29",
    "sleep_apnea": "G47.33",
}

# ─────────────────────────────────────────────────────────────────
# REVERSE SYNONYM MAP: synonym/abbreviation → canonical_name
# Auto-generated from SYNONYM_MAP for O(1) lookup.
# ─────────────────────────────────────────────────────────────────

REVERSE_SYNONYM_MAP: dict[str, str] = {}
for _canonical, _synonyms in SYNONYM_MAP.items():
    # Map the canonical name to itself
    REVERSE_SYNONYM_MAP[_canonical.lower().replace("_", " ")] = _canonical
    # Map each synonym to the canonical name
    for _syn in _synonyms:
        REVERSE_SYNONYM_MAP[_syn.lower()] = _canonical


def resolve_to_canonical(term: str) -> str | None:
    """Resolve a medical term to its canonical name.

    Returns None if no match found.

    >>> resolve_to_canonical("HTN")
    'hypertension'
    >>> resolve_to_canonical("heart attack")
    'myocardial_infarction'
    >>> resolve_to_canonical("unknown thing")
    """
    normalized = term.lower().strip()
    return REVERSE_SYNONYM_MAP.get(normalized)


def get_icd10(term: str) -> str | None:
    """Get ICD-10 code for a medical term (resolves synonyms).

    >>> get_icd10("HTN")
    'I10'
    >>> get_icd10("type 2 diabetes")
    'E11.9'
    """
    canonical = resolve_to_canonical(term)
    if canonical:
        return ICD10_CODES.get(canonical)
    return ICD10_CODES.get(term.lower().strip().replace(" ", "_"))
