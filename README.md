---
title: Medical Record Abstraction Env
emoji: ⚕️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 8000
---

# Medical Record Abstraction Environment

A production-ready OpenEnv-compliant reinforcement learning environment for **medical record abstraction** — the process of extracting structured clinical data from unstructured patient notes.

## 🏥 Overview

Agents interact with synthetic clinical notes through a command-based interface, progressively tackling harder extraction tasks:

| Task | Difficulty | What the Agent Extracts | Max Steps |
|------|-----------|------------------------|-----------|
| **Task 1** | Easy | Demographics, chief complaint, vital signs | 5 |
| **Task 2** | Medium | Diagnoses + ICD-10, medications, drug conflicts | 8 |
| **Task 3** | Hard | Risk level, critical flags, readmission score, clinical summary | 10 |

Each task is graded by a **deterministic grader** producing scores in `[0.0, 1.0]` with detailed component breakdowns.

## 🎯 Key Features

- **Real-world task**: Medical record abstraction is performed daily by clinical coders, auditors, and health IT systems
- **24 synthetic clinical notes** (8 per task) covering cardiology, pulmonology, endocrinology, neurology, and more
- **47 medical conditions** with ICD-10 codes and synonym mappings (HTN↔hypertension, MI↔heart attack)
- **30 drug interactions** (15 drug-allergy conflicts + 15 drug-drug interactions) planted across notes
- **Continuous reward signal** with exploration bonuses and redundancy penalties
- **Pure Python graders** — no external NLP deps (uses `difflib`, custom F1, ROUGE-L)

## 🔌 Action / Observation Spaces

### Action Space

```python
class MedicalRecordAction(Action):
    command: str   # "get_task" | "get_note" | "get_drugs" | "get_guidelines" | "submit"
    data: str      # JSON payload (for "submit" only)
```

### Observation Space

```python
class MedicalRecordObservation(Observation):
    task_id: str                      # "task_1", "task_2", "task_3"
    task_description: str             # What to extract + output schema
    clinical_note: str                # Raw patient note text
    drug_database: str                # Drug interaction reference (Task 2+)
    clinical_guidelines: str          # Risk assessment criteria (Task 3)
    message: str                      # Environment feedback
    score_breakdown: Dict[str, float] # Grading components on submission
    available_commands: List[str]     # Dynamic action masking
    step_number: int                  # Current step
    max_steps: int                    # Step limit
    done: bool                        # Episode terminated?
    reward: float                     # Step reward
```

## 📊 Grading Details

### Task 1: Basic Extraction
| Component | Weight | Method |
|-----------|--------|--------|
| Patient name | 15% | Fuzzy string match (≥0.85) |
| Age | 10% | Exact numeric |
| Sex | 10% | First-letter match |
| Chief complaint | 20% | Fuzzy match (≥0.50) |
| Onset date | 15% | Date string match |
| Vital signs | 30% | Numeric with tolerance (±2 HR, ±0.5°F, etc.) |

### Task 2: Entity Extraction + Validation
| Component | Weight | Method |
|-----------|--------|--------|
| Diagnoses F1 | 25% | Entity F1 with medical synonym resolution |
| ICD-10 accuracy | 15% | Exact code match per diagnosis |
| Medications F1 | 15% | Drug name fuzzy match |
| Inconsistency detection | 30% | Recall of planted drug conflicts |
| Allergies | 5% | Set recall |
| Format validity | 10% | Required keys present |

### Task 3: Risk Assessment
| Component | Weight | Method |
|-----------|--------|--------|
| Risk level | 20% | Exact match (high/medium/low) |
| Risk factors | 15% | Fuzzy recall |
| Critical flags | 25% | Flag recall (fuzzy ≥0.40) |
| Readmission score | 15% | Proximity (±0.5 tolerance) |
| Clinical summary | 25% | ROUGE-L F1 |

## 🚀 Setup & Running

This environment is fully verified and packaged. It can be run locally via standard Python virtual environments, or containerized via Docker.

### 1. Clone & Install
```bash
git clone https://github.com/your-username/medical-record-env.git
cd medical-record-env

# Create and activate a virtual environment (Recommended)
python -m venv venv
source venv/bin/activate  # Or `venv\Scripts\activate` on Windows

# Install the environment, solvers, and dependencies natively
pip install -e .
```

### 2. Configure Credentials (.env)
We securely read credentials from your environment or a `.env` file. **Before running inference**, duplicate the securely provided template:
```bash
# Copy the secure template
cp .env.example .env
```
Now, configure `.env` with your desired endpoint:
```yaml
API_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4o-mini
HF_TOKEN=sk-your-api-key
```

### 3. Run Inference & Testing
```bash
# Verify the mathematical graders (53 tests)
pytest tests/ -v

# Run the OpenEnv Validation protocol
openenv validate

# Run your baseline agent!
python inference.py
```

### 4. Interactive Web Server & Docker
You can hit the API endpoint identically to how Hackathon Agents will test it over the cloud!

**Run via Uvicorn (FastAPI):**
```bash
uvicorn server.app:app --host 0.0.0.0 --port 8000
# Open http://127.0.0.1:8000/docs for the beautiful interactive Swagger UI Sandbox!
```

**Run via Docker (Pristine Container):**
```bash
docker build -f server/Dockerfile -t medical_record_abstraction_env .
docker run -p 8000:8000 medical_record_abstraction_env
```

## 📁 Project Structure

```text
medical_record_abstraction_env/
├── openenv.yaml                    # OpenEnv manifest
├── pyproject.toml                  # Package config
├── uv.lock                         # Strict dependency map
├── .env.example                    # Secure API Key template
├── .gitignore                      # Repository safety blockers
├── .dockerignore                   # Docker build filters
├── inference.py                    # Baseline inference script
├── models.py                       # Action, Observation, State models
├── client.py                       # EnvClient subclass
├── __init__.py                     # Package exports
├── README.md                       # Full documentation
├── data/
│   ├── synthetic_notes.py          # 24 clinical notes with ground truth
│   ├── medical_ontology.py         # 47 conditions, ICD-10, synonyms
│   └── drug_interactions.py        # 30 planted drug interactions
├── server/
│   ├── app.py                      # FastAPI application via create_app()
│   ├── environment.py              # Environment (step/reset/state)
│   ├── graders.py                  # Deterministic grading system (F1, ROUGE-L)
│   ├── reward.py                   # Continuous reward shaping
│   ├── tasks.py                    # Task configs + clinical guidelines
│   ├── Dockerfile                  # Container deployment config
│   └── requirements.txt            # Local snapshot dependencies
├── tests/
│   ├── test_env.py                 # Environment tests (24 items)
│   └── test_graders.py             # Grader tests (29 items)
└── examples/
    ├── sample_note.txt             # Example clinical note
    └── expected_output.json        # Expected extraction outputs
```

## 🔄 Episode Flow

```
Agent                          Environment
  │                               │
  │──── reset(task_id) ──────────>│  Initialize episode
  │<── observation ───────────────│  Available commands, context
  │                               │
  │──── step(get_task) ──────────>│  +0.02 reward
  │<── task_description ─────────│  Output schema, scoring
  │                               │
  │──── step(get_note) ──────────>│  +0.02 reward
  │<── clinical_note ────────────│  Patient data
  │                               │
  │──── step(get_drugs) ─────────>│  +0.02 reward (Task 2+)
  │<── drug_database ────────────│  Interaction reference
  │                               │
  │──── step(submit, JSON) ──────>│  Graded score [0.0-1.0]
  │<── score_breakdown, done ────│  Episode complete
```

## 📝 License

This project uses synthetic clinical data. No real patient information is included.
