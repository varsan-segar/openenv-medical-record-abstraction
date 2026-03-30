"""
Medical Record Environment — Data Layer.

Provides synthetic clinical notes, medical ontology, and drug interaction
databases for the environment's three tasks.
"""

from .medical_ontology import SYNONYM_MAP, ICD10_CODES, REVERSE_SYNONYM_MAP
from .drug_interactions import DRUG_ALLERGY_CONFLICTS, DRUG_DRUG_INTERACTIONS
from .synthetic_notes import NOTES_BY_TASK, get_note, get_all_notes_for_task

__all__ = [
    "SYNONYM_MAP",
    "ICD10_CODES",
    "REVERSE_SYNONYM_MAP",
    "DRUG_ALLERGY_CONFLICTS",
    "DRUG_DRUG_INTERACTIONS",
    "NOTES_BY_TASK",
    "get_note",
    "get_all_notes_for_task",
]
