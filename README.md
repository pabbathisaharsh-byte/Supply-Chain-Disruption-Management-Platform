# 🛡️ SecureOps AI - Security Operations Center (SOC) Assistant

SecureOps AI is an enterprise-grade, AI-powered Security Operations Center (SOC) Assistant designed to help security analysts autonomously hunt threats, correlate logs across multiple enterprise security directories, orchestrate workflow responses, and validate destructive or critical actions via an interactive human-in-the-loop (HITL) gate.

The application leverages local **Llama 3.2** LLM inference (via Ollama) with a highly robust local JSON database backup fallback, ensuring responsive, resilient, and highly secure operations inside disconnected and sensitive environments.

---

## 👥 SOC Engineering Team & Roles

The codebase is organized in a modular structure to match the deliverables of all four SOC consulting team engineering roles:

1. **AI Conversation Engineer (Team Member 1)**
   * **Scope:** UI Layout (`app/ui/chat.py`) & System Prompts (`app/prompts/system_prompts.py`).
   * **Duties:** Implemented conversation memory persistence, CSS aesthetic modules, and prompt guards defining agent parameters.
2. **Tool & Integration Engineer (Team Member 2)**
   * **Scope:** REST APIs / local Databases (`app/tools/`).
   * **Duties:** Engineered the SIEM Alert lookups (`alert_tools.py`), IAM User activities (`identity_tools.py`), Endpoint statuses (`endpoint_tools.py`), Ticketing workflows (`incident_tools.py`), and Report writers (`reporting_tools.py`).
3. **Agent Engineer (Team Member 3)**
   * **Scope:** LangGraph structures (`app/workflow/graph.py`) & Gated locks (`app/workflow/human_in_the_loop.py`).
   * **Duties:** Configured the state machine dictionaries, node processing pathways, and Human-in-the-loop validation barriers.
4. **Multi-Agent Engineer (Team Member 4)**
   * **Scope:** Router Supervision (`app/agents/supervisor.py`) & Specialist Nodes (`app/agents/specialists.py`).
   * **Duties:** Designed the Supervisor Agent routing rules and formulated domain-specialist node outputs.

---

## 🗺️ Project Folder Layout

```
.
├── app/
│   ├── agents/
│   │   ├── specialists.py       # Specialist agents (Alert, Endpoint, Identity, Incident, Reporting)
│   │   └── supervisor.py        # Central Supervisor router node
│   ├── data/
│   │   ├── alerts.json          # Mock SIEM alerts database
│   │   ├── endpoint_assets.json # Mock EDR assets database
│   │   ├── logins.json          # Mock IAM logins database
│   │   ├── user_activities.json # Mock IAM user actions database
│   │   ├── incidents.json       # Mock incidents database
│   │   └── reports.json         # Mock reports database
│   ├── evaluation/
│   │   └── langsmith_eval.py    # LangSmith tracing hookups
│   ├── prompts/
│   │   └── system_prompts.py    # System prompt collections
│   ├── tests/
│   │   └── test_structure.py    # Unit & Integration test suite
│   ├── tools/
│   │   ├── alert_tools.py       # Alert lookup database wrapper
│   │   ├── correlation_tools.py # Phase 2 Correlation Engine (5 Multi-Stage Threat Scenarios)
│   │   ├── endpoint_tools.py    # EDR asset lookup wrapper
│   │   ├── identity_tools.py    # IAM logs lookup wrapper
│   │   ├── incident_tools.py    # Ticketing database wrapper
│   │   └── reporting_tools.py   # Investigation report writer
│   ├── ui/
│   │   └── chat.py              # Gorgeous Streamlit Chat & Telemetry Dashboard
│   ├── config.py                # Environment configurations & model fallbacks
│   └── main.py                  # Entry Point
├── requirements.txt             # Python project dependencies
└── README.md                    # System documentation
```

---

## ⚡ Key Features

### 1. Unified SOC Workstation Dashboard
An executive Streamlit-based UI displaying real-time telemetry metrics (active sources, campaigns, active LLM core, system health compliant statuses) and a split screen separating interactive multi-agent chat and real-time incident queue updates.

### 2. local Llama 3.2 Integration & Dynamic Fallbacks
The specialized agents dynamically invoke Ollama's local `llama3.2` model endpoint (`http://localhost:11434/v1`) to summarize logs and draft recommendations. If Ollama is offline or unreachable, the agents fall back gracefully to a highly advanced, local Python parser that checks and compares alert/workstation/user existence in JSON databases, dynamically outputting "not found" alerts instead of statically defaulting parameters.

### 3. Human-in-the-Loop Gating
Destructive or highly critical mutations halt execution and request analyst validation in the chat window before making database changes:
* Creating an incident ticket.
* Escalating tickets to Tier 3.
* Closing incident investigations.
* Writing or dispatching final investigation reports.

### 4. Phase 2 Threat Correlation Engine
Includes a threat-hunting module (`app/tools/correlation_tools.py`) that correlates isolated alerts into **5 distinct multi-stage campaigns** with risk scores and explainable AI reasoning:
1. **Compromised Credentials with Foreign Access** (IAM session hijack leading to endpoint EDR Trojan and firewall data exfiltration).
2. **Malware with High-bandwidth Firewall Callback** (EDR Trojan executing outbound transfers).
3. **Privilege Account Outside Normal Working Hours** (Admin login at 03:15 AM triggering an Active Directory database dump).
4. **Unmanaged Device Access** (EDR-inactive workstation using Tor exit nodes).
5. **Ransomware Preparation Sequence** (PowerShell disabling volume shadow copies immediately followed by file encryption patterns).

---

## 🚀 Installation & Local Running

### 1. Clone the repository and set up a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. (Optional) Run Ollama and pull Llama 3.2 locally:
Ensure Ollama is installed on your local host machine, then run:
```bash
ollama run llama3.2
```
*Note: If Ollama is not running, the platform operates seamlessly using dynamic local fallback parsers.*

### 4. Run the Streamlit Dashboard:
```bash
streamlit run app/ui/chat.py
```

### 5. Run the Automated Test Suite:
To execute structural, routing, data lookup, and human-in-the-loop integration checks, execute:
```bash
python3 -m unittest discover -s app/tests -p "test_*.py"
```
