# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
FastAPI application for the Medical Record Abstraction Environment.

Exposes the MedicalRecordEnvironment over HTTP and WebSocket endpoints.

Endpoints:
    - POST /reset: Reset the environment
    - POST /step: Execute an action
    - GET /state: Get current environment state
    - GET /schema: Get action/observation schemas
    - WS /ws: WebSocket endpoint for persistent sessions

Usage:
    # Development (with auto-reload):
    uvicorn server.app:app --reload --host 0.0.0.0 --port 8000

    # Production:
    uvicorn server.app:app --host 0.0.0.0 --port 8000 --workers 4
"""

try:
    from openenv.core.env_server.http_server import create_app
except Exception as e:  # pragma: no cover
    raise ImportError(
        "openenv is required for the web interface. Install dependencies with '\n    uv sync\n'"
    ) from e

try:
    from ..models import MedicalRecordAction, MedicalRecordObservation
    from .environment import MedicalRecordEnvironment
except (ImportError, ModuleNotFoundError):
    from models import MedicalRecordAction, MedicalRecordObservation
    from server.environment import MedicalRecordEnvironment


# Create the app with web interface and README integration
app = create_app(
    MedicalRecordEnvironment,
    MedicalRecordAction,
    MedicalRecordObservation,
    env_name="medical_record_abstraction_env",
    max_concurrent_envs=1,
)

app.title = "Medical Record Abstraction OpenEnv API"
app.version = "1.0.0"
app.description = """
### 🩺 Medical Record Extraction Environment
This is an **OpenEnv-compliant API** that hosts the Medical Record Abstraction RL environment. It simulates the real-world workflow of clinical coders parsing unstructured patient notes into structured JSON.

#### 📊 Available Tasks
1. **Task 1 (Easy)** - Abstract Demographic Data & Vitals.
2. **Task 2 (Medium)** - Extract Diagnoses (ICD-10) and Detect Drug Conflicts.
3. **Task 3 (Hard)** - Clinical Risk Assessment & Readmission Scoring.

#### 🚀 How Judges & Agents Use This
Agent evaluators send an HTTP POST to `/env/reset` to initialize an episode, and then send repeated POSTs to `/env/step` containing `MedicalRecordAction` commands until the episode completes.
"""


@app.get("/")
def read_root():
    """Root endpoint verifying that the OpenEnv space is active."""
    return {
        "status": "success",
        "message": "Welcome to the Medical Record Abstraction OpenEnv! The environment is running perfectly.",
        "docs": "/docs",
        "health": "/health"
    }


def main(host: str = "0.0.0.0", port: int = 8000):
    """Entry point for direct execution."""
    import uvicorn

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
