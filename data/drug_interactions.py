"""
Drug Interactions Database — Drug-allergy conflicts and drug-drug interactions.

Provides deterministic, well-documented interaction data for Task 2 & 3 grading.
All interactions are based on real clinical pharmacology references.
"""

# ─────────────────────────────────────────────────────────────────
# DRUG-ALLERGY CONFLICTS
# Cross-reactivity between drug classes and known allergies.
# ─────────────────────────────────────────────────────────────────

DRUG_ALLERGY_CONFLICTS: list[dict] = [
    # Penicillin class cross-reactivity
    {
        "drug": "amoxicillin",
        "allergy": "penicillin",
        "severity": "high",
        "reason": "Amoxicillin is a penicillin-class antibiotic. "
                  "Cross-reactivity rate ~100% in penicillin-allergic patients.",
    },
    {
        "drug": "ampicillin",
        "allergy": "penicillin",
        "severity": "high",
        "reason": "Ampicillin is a penicillin-class antibiotic with direct cross-reactivity.",
    },
    {
        "drug": "piperacillin",
        "allergy": "penicillin",
        "severity": "high",
        "reason": "Piperacillin shares the beta-lactam ring structure with penicillin.",
    },
    # Cephalosporin–penicillin cross-reactivity
    {
        "drug": "cephalexin",
        "allergy": "penicillin",
        "severity": "medium",
        "reason": "Cephalosporins have ~2-5% cross-reactivity with penicillin allergy "
                  "due to shared beta-lactam ring.",
    },
    {
        "drug": "ceftriaxone",
        "allergy": "penicillin",
        "severity": "medium",
        "reason": "Third-generation cephalosporin with low but clinically significant "
                  "cross-reactivity with penicillin allergy.",
    },
    # NSAID cross-sensitivity
    {
        "drug": "ibuprofen",
        "allergy": "aspirin",
        "severity": "medium",
        "reason": "NSAIDs share cyclooxygenase inhibition pathway. "
                  "Cross-sensitivity rate ~10-25% in aspirin-allergic patients.",
    },
    {
        "drug": "naproxen",
        "allergy": "aspirin",
        "severity": "medium",
        "reason": "NSAID cross-sensitivity with aspirin allergy via COX inhibition.",
    },
    {
        "drug": "ketorolac",
        "allergy": "aspirin",
        "severity": "medium",
        "reason": "Potent NSAID with cross-reactivity risk in aspirin-sensitive patients.",
    },
    # Sulfonamide cross-reactivity
    {
        "drug": "sulfamethoxazole",
        "allergy": "sulfa",
        "severity": "high",
        "reason": "Direct sulfonamide antibiotic. Contraindicated in sulfa allergy.",
    },
    {
        "drug": "trimethoprim-sulfamethoxazole",
        "allergy": "sulfa",
        "severity": "high",
        "reason": "Contains sulfamethoxazole. Contraindicated in sulfa allergy. "
                  "Also known as Bactrim/Septra.",
    },
    # ACE inhibitor angioedema
    {
        "drug": "lisinopril",
        "allergy": "ace_inhibitors",
        "severity": "high",
        "reason": "ACE inhibitor-induced angioedema can be life-threatening. "
                  "All ACE inhibitors are contraindicated after angioedema episode.",
    },
    {
        "drug": "enalapril",
        "allergy": "ace_inhibitors",
        "severity": "high",
        "reason": "Class-wide contraindication for ACE inhibitor angioedema history.",
    },
    # Statin myopathy
    {
        "drug": "atorvastatin",
        "allergy": "statins",
        "severity": "medium",
        "reason": "History of statin-induced rhabdomyolysis. "
                  "Consider alternative lipid-lowering therapy.",
    },
    # Contrast dye
    {
        "drug": "iodinated_contrast",
        "allergy": "contrast_dye",
        "severity": "high",
        "reason": "Prior anaphylactoid reaction to iodinated contrast. "
                  "Requires premedication protocol or alternative imaging.",
    },
    # Opioid allergy
    {
        "drug": "codeine",
        "allergy": "morphine",
        "severity": "medium",
        "reason": "Codeine is metabolized to morphine. Cross-reactivity expected "
                  "in morphine-allergic patients.",
    },
]

# ─────────────────────────────────────────────────────────────────
# DRUG-DRUG INTERACTIONS
# Clinically significant interactions that agents should detect.
# ─────────────────────────────────────────────────────────────────

DRUG_DRUG_INTERACTIONS: list[dict] = [
    # Bleeding risk
    {
        "drug_a": "warfarin",
        "drug_b": "aspirin",
        "severity": "high",
        "effect": "Significantly increased bleeding risk. Both affect hemostasis "
                  "via different mechanisms (coagulation cascade + platelet inhibition).",
    },
    {
        "drug_a": "warfarin",
        "drug_b": "ibuprofen",
        "severity": "high",
        "effect": "NSAIDs increase anticoagulant effect of warfarin and add GI "
                  "bleeding risk via COX-1 inhibition.",
    },
    {
        "drug_a": "warfarin",
        "drug_b": "fluconazole",
        "severity": "high",
        "effect": "Fluconazole inhibits CYP2C9, dramatically increasing warfarin levels. "
                  "INR monitoring essential.",
    },
    {
        "drug_a": "clopidogrel",
        "drug_b": "omeprazole",
        "severity": "medium",
        "effect": "Omeprazole inhibits CYP2C19, reducing conversion of clopidogrel "
                  "to its active metabolite. Use pantoprazole instead.",
    },
    # Hyperkalemia risk
    {
        "drug_a": "lisinopril",
        "drug_b": "spironolactone",
        "severity": "high",
        "effect": "Both increase potassium levels. Combined use significantly increases "
                  "hyperkalemia risk. Monitor potassium closely.",
    },
    {
        "drug_a": "lisinopril",
        "drug_b": "potassium_chloride",
        "severity": "medium",
        "effect": "ACE inhibitor reduces potassium excretion. Supplemental potassium "
                  "may cause dangerous hyperkalemia.",
    },
    # Serotonin syndrome
    {
        "drug_a": "sertraline",
        "drug_b": "tramadol",
        "severity": "high",
        "effect": "Both increase serotonergic activity. Combined use increases risk "
                  "of serotonin syndrome (hyperthermia, rigidity, clonus).",
    },
    {
        "drug_a": "fluoxetine",
        "drug_b": "linezolid",
        "severity": "high",
        "effect": "Linezolid is a reversible MAO inhibitor. Combined with SSRI, "
                  "high risk of serotonin syndrome.",
    },
    # QT prolongation
    {
        "drug_a": "amiodarone",
        "drug_b": "ciprofloxacin",
        "severity": "high",
        "effect": "Both prolong QT interval. Combined use increases risk of "
                  "torsades de pointes and sudden cardiac death.",
    },
    {
        "drug_a": "haloperidol",
        "drug_b": "methadone",
        "severity": "high",
        "effect": "Additive QT prolongation. Combined use requires ECG monitoring.",
    },
    # Renal toxicity
    {
        "drug_a": "metformin",
        "drug_b": "iodinated_contrast",
        "severity": "high",
        "effect": "Contrast-induced nephropathy can impair metformin clearance, "
                  "leading to lactic acidosis. Hold metformin 48h before/after contrast.",
    },
    {
        "drug_a": "gentamicin",
        "drug_b": "vancomycin",
        "severity": "high",
        "effect": "Both are nephrotoxic. Combined use significantly increases "
                  "risk of acute kidney injury. Monitor renal function and drug levels.",
    },
    {
        "drug_a": "ibuprofen",
        "drug_b": "lisinopril",
        "severity": "medium",
        "effect": "NSAIDs reduce renal blood flow and can decrease ACE inhibitor "
                  "efficacy. Also increases AKI risk in volume-depleted patients.",
    },
    # Hepatotoxicity
    {
        "drug_a": "methotrexate",
        "drug_b": "trimethoprim-sulfamethoxazole",
        "severity": "high",
        "effect": "Both are folate antagonists. Combined use causes severe "
                  "pancytopenia and hepatotoxicity.",
    },
    # Hypoglycemia
    {
        "drug_a": "glipizide",
        "drug_b": "fluconazole",
        "severity": "high",
        "effect": "Fluconazole inhibits CYP2C9 metabolism of sulfonylureas, "
                  "causing prolonged and severe hypoglycemia.",
    },
]


def check_drug_allergy_conflicts(
    medications: list[str],
    allergies: list[str],
) -> list[dict]:
    """Check for drug-allergy conflicts given lists of medications and allergies.

    Args:
        medications: List of drug names (case-insensitive).
        allergies: List of allergy names (case-insensitive).

    Returns:
        List of conflict dicts found.

    >>> conflicts = check_drug_allergy_conflicts(["amoxicillin"], ["penicillin"])
    >>> len(conflicts)
    1
    >>> conflicts[0]["severity"]
    'high'
    """
    meds_lower = {m.lower().strip() for m in medications}
    allergies_lower = {a.lower().strip() for a in allergies}

    found = []
    for conflict in DRUG_ALLERGY_CONFLICTS:
        if (conflict["drug"].lower() in meds_lower
                and conflict["allergy"].lower() in allergies_lower):
            found.append(conflict)
    return found


def check_drug_drug_interactions(
    medications: list[str],
) -> list[dict]:
    """Check for drug-drug interactions within a medication list.

    Args:
        medications: List of drug names (case-insensitive).

    Returns:
        List of interaction dicts found.

    >>> interactions = check_drug_drug_interactions(["warfarin", "aspirin"])
    >>> len(interactions)
    1
    >>> interactions[0]["severity"]
    'high'
    """
    meds_lower = {m.lower().strip() for m in medications}

    found = []
    for interaction in DRUG_DRUG_INTERACTIONS:
        if (interaction["drug_a"].lower() in meds_lower
                and interaction["drug_b"].lower() in meds_lower):
            found.append(interaction)
    return found


def get_drug_database_text() -> str:
    """Format the drug interaction database as text for the agent.

    Returns a human-readable string containing all known interactions.
    """
    lines = ["=== DRUG-ALLERGY CONFLICT DATABASE ===\n"]
    for c in DRUG_ALLERGY_CONFLICTS:
        lines.append(
            f"• Drug: {c['drug']} | Allergy: {c['allergy']} | "
            f"Severity: {c['severity']}\n  Reason: {c['reason']}"
        )

    lines.append("\n\n=== DRUG-DRUG INTERACTION DATABASE ===\n")
    for i in DRUG_DRUG_INTERACTIONS:
        lines.append(
            f"• {i['drug_a']} + {i['drug_b']} | Severity: {i['severity']}\n"
            f"  Effect: {i['effect']}"
        )

    return "\n".join(lines)
