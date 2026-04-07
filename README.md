---
title: Medical Record Abstraction Env
emoji: ⚕️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 8000
---

# Medical Record Abstraction Environment

An OpenEnv-compliant reinforcement learning environment for extracting structured clinical data from unstructured patient notes.

## Quick Start

```bash
# Clone and install
git clone https://github.com/varsan-segar/openenv-medical-record-abstraction.git
cd openenv-medical-record-abstraction
pip install -e .

# Configure credentials
cp .env.example .env
# Edit .env with your API_BASE_URL, MODEL_NAME, and HF_TOKEN

# Run inference
python inference.py

# Run tests
pytest tests/ -v

# Validate environment
openenv validate
```

### Docker

```bash
docker build -t medical_record_abstraction_env .
docker run -p 8000:8000 medical_record_abstraction_env
```

### Environment Variables

| Variable | Required | Default |
|----------|----------|---------|
| `API_BASE_URL` | No | `https://api.openai.com/v1` |
| `MODEL_NAME` | No | `gpt-4o-mini` |
| `HF_TOKEN` | Yes | — |
| `OPENAI_API_KEY` | No | Fallback if `HF_TOKEN` is not set |

---

## Overview

Agents interact with synthetic clinical notes through a command-based interface across three tasks:

| Task | Difficulty | Extraction Target | Max Steps |
|------|-----------|-------------------|-----------|
| Task 1 | Easy | Demographics, chief complaint, vital signs | 5 |
| Task 2 | Medium | Diagnoses + ICD-10, medications, drug conflicts | 8 |
| Task 3 | Hard | Risk level, critical flags, readmission score, clinical summary | 10 |

## Action and Observation Spaces

### Action

```python
class MedicalRecordAction(Action):
    command: str   # "get_task" | "get_note" | "get_drugs" | "get_guidelines" | "submit"
    data: str      # JSON payload (for "submit" only)
```

### Observation

```python
class MedicalRecordObservation(Observation):
    task_id: str
    task_description: str
    clinical_note: str
    drug_database: str
    clinical_guidelines: str
    message: str
    score_breakdown: Dict[str, float]
    available_commands: List[str]
    step_number: int
    max_steps: int
    done: bool
    reward: float
```

## Grading

All graders are deterministic and use only the Python standard library.

**Task 1** — Fuzzy string match for names and complaints, exact match for age/sex, numeric tolerance for vitals.

**Task 2** — Entity-level F1 with medical synonym resolution (47 conditions, ICD-10 codes), drug interaction recall across 30 planted conflicts.

**Task 3** — Exact match for risk level, fuzzy recall for risk factors and critical flags, proximity scoring for readmission risk, ROUGE-L F1 for clinical summary.

## Episode Flow

```
Agent                          Environment
  |                               |
  |---- reset(task_id) ---------->|  Initialize episode
  |<-- observation ---------------|
  |                               |
  |---- step(get_task) ---------->|  +0.02 reward
  |<-- task_description ----------|
  |                               |
  |---- step(get_note) ---------->|  +0.02 reward
  |<-- clinical_note -------------|
  |                               |
  |---- step(submit, JSON) ------>|  Graded score [0.0-1.0]
  |<-- score_breakdown, done -----|
```

## Project Structure

```
medical_record_abstraction_env/
├── inference.py          # Baseline inference script
├── models.py             # Action, Observation, State models
├── client.py             # EnvClient subclass
├── Dockerfile            # Container deployment config
├── openenv.yaml          # OpenEnv manifest
├── pyproject.toml        # Package config
├── data/
│   ├── synthetic_notes.py    # 24 clinical notes with ground truth
│   ├── medical_ontology.py   # 47 conditions, ICD-10, synonyms
│   └── drug_interactions.py  # 30 planted drug interactions
├── server/
│   ├── app.py            # FastAPI application
│   ├── environment.py    # Environment (step/reset/state)
│   ├── graders.py        # Deterministic grading (F1, ROUGE-L)
│   ├── reward.py         # Continuous reward shaping
│   └── tasks.py          # Task configs and guidelines
└── tests/
    ├── test_env.py       # Environment tests
    └── test_graders.py   # Grader tests
```

## License

This project uses synthetic clinical data. No real patient information is included.
