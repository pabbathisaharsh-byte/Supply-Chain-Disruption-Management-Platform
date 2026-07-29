# Supply-Chain-Disruption-Management-Platform

## Overview

SecureOps AI is a simulated Security Operations Center (SOC) platform for managing supply-chain disruption scenarios using a multi-agent workflow. This repository is the Phase 2 enhancement for the SecureOps AI project, with a focus on AI-powered threat hunting and event correlation.

The app combines:

- A Streamlit-based analyst chat interface
- A supervisor agent that routes requests to specialist agents
- Mock telemetry data for SIEM, EDR, IAM, and incident management
- Human-in-the-loop gating for critical actions
- AI-driven alert summarization, endpoint investigation, identity review, incident management, and report generation
- Phase 2 correlation capabilities supporting at least five distinct investigation scenarios

## Architecture

The repository is organized into the following core components:

- `main.py` — Application entry point and UI launcher
- `app/config.py` — Environment configuration and LLM default settings
- `app/ui/chat.py` — Streamlit chat interface, session state, action buttons, and approval workflow
- `app/agents/supervisor.py` — Query routing logic for deciding which specialist agent to invoke
- `app/agents/specialists.py` — Domain-specific agent behavior for alerts, endpoints, identity, incidents, and reporting
- `app/workflow/graph.py` — Multi-agent workflow execution and state management
- `app/workflow/human_in_the_loop.py` — Approval gate logic for sensitive mutations
- `app/tools/` — Mock service adapters for alerts, identity, endpoints, incidents, and reports
- `app/data/` — Local JSON data stores used by the mock backend tools
- `app/tests/test_structure.py` — Basic repository structure test

## Features

- Keyword-based supervisor routing to:
  - `alert_agent` for SIEM/firewall alerts
  - `endpoint_agent` for workstation/EDR status
  - `identity_agent` for IAM/login activity
  - `incident_agent` for ticket creation, escalation, and status lookup
  - `reporting_agent` for investigation reports and correlation scenarios
- Mock data-driven insights from local JSON datasets
- Phase 2 event correlation and threat hunting summaries
- Gated approval for:
  - incident creation
  - incident escalation
  - investigation closure
  - final report generation
  - alert severity updates

## Local Data Stores

The app reads and updates local JSON files under `app/data/`:

- `alerts.json`
- `endpoint_assets.json`
- `logins.json`
- `user_activities.json`
- `incidents.json`
- `reports.json`

## Application Link

https://supply-chain-disruption-management-platform-9shb4fmsv9szkgi3mn.streamlit.app/

## Technology Stack

- Frontend/UI - Streamlit
- Language - Python
- LLM Orchestration - LangChain
- Workflow - LangGraph
- LLM Integration - LangChain-OpenAI
- Data Validation - Pydantic
- Document Processing - PyPDF
- Framework - Pytest

## Results

<img width="1920" height="1080" alt="Screenshot (2)" src="https://github.com/user-attachments/assets/2e240ee1-e2ed-4fee-8d7e-adf418828fab" />
<img width="1920" height="1080" alt="Screenshot (3)" src="https://github.com/user-attachments/assets/a6b90f62-ff13-4522-8883-764b4c75e7b8" />
<img width="1920" height="1080" alt="Screenshot (4)" src="https://github.com/user-attachments/assets/a713ca2b-8fa2-4a21-b04e-b82c7b3abc9c" />
<img width="1920" height="1080" alt="Screenshot (5)" src="https://github.com/user-attachments/assets/00e57078-3755-4380-9900-4a1088c223a2" />
<img width="1920" height="1080" alt="Screenshot (6)" src="https://github.com/user-attachments/assets/df67955d-ab7c-4ffc-95bc-cdbc1c27c605" />
<img width="1920" height="1080" alt="Screenshot (7)" src="https://github.com/user-attachments/assets/7c650ca6-f122-4111-b96c-ea983af03443" />






## Installation

1. Create and activate a Python environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Configure environment variables:

```bash
set SIEM_API_ENDPOINT=https://api.mocksiem.local/v1
set EDR_API_ENDPOINT=https://api.mockedr.local/v1
set IAM_API_ENDPOINT=https://api.mockiam.local/v1
set LLM_MODEL=llama3.2
set LLM_TEMPERATURE=0.0
```

If environment variables are not set, the app uses built-in defaults.

## Running the App

Start the Streamlit interface with either:

```bash
streamlit run main.py
```

or:

```bash
python main.py
```

The UI exposes a chat workflow plus sidebar quick commands and approval gating.

## Usage

Example analyst prompts:

- `show security alerts`
- `investigate workstation WS-900 status`
- `check logins for jdoe`
- `create security incident`
- `escalate incident INC-2024-101`
- `correlate events and find threat hunting campaigns`

The system automatically routes the query to the correct specialist agent based on keywords.

## Testing

Run the repository test suite with:

```bash
pytest
```

## Notes

- This project is a simulation and uses local JSON mock data rather than real external services.
- The default model is `llama3.2`, and it is configured in `app/config.py`.
- Human-in-the-loop actions are required before the app performs any sensitive incident or report changes.
