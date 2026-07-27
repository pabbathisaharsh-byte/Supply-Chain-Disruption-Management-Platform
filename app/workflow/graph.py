# app/workflow/graph.py
"""
Purpose: Agent Engineer (Team Member 3)
Role:
- Formulates the LangGraph state machine workflow.
- Defines state management, edge routers, and agent nodes.
- Integrates the supervisor agent and sub-agents into a unified reactive graph.
"""

from app.agents.specialists import (
    alert_analysis_agent,
    endpoint_agent,
    identity_agent,
    incident_agent,
    reporting_agent,
)
from app.agents.supervisor import route_request
from app.workflow.human_in_the_loop import request_human_approval


class StateDict(dict):
    """
    State tracking schema for the LangGraph workflow.
    Ensures clear variables like user_message, agent_response, approval_needed, and error_logs.
    """
    user_message: str
    conversation_history: list
    current_agent: str
    agent_response: str
    approval_needed: bool
    approved: bool
    error_logs: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setdefault("conversation_history", [])
        self.setdefault("current_agent", "")
        self.setdefault("agent_response", "")
        self.setdefault("approval_needed", False)
        self.setdefault("approved", False)
        self.setdefault("error_logs", "")


def build_workflow_graph():
    """
    Sets up the LangGraph nodes, edges, conditional pathways,
    incorporates error handling, and compiles the workflow.
    """

    def run_workflow(state):
        workflow_state = StateDict(state)
        workflow_state.setdefault("conversation_history", [])

        user_message = workflow_state.get("user_message", "")
        if user_message:
            history = list(workflow_state.get("conversation_history", []))
            history.append({"role": "user", "content": user_message})
            workflow_state["conversation_history"] = history

        route = route_request(workflow_state)
        workflow_state["current_agent"] = route
        workflow_state["approval_needed"] = False
        workflow_state["approved"] = False
        workflow_state["agent_response"] = ""
        workflow_state["error_logs"] = ""

        if route in {"incident_agent", "reporting_agent"}:
            action_type = "CREATE_INCIDENT" if route == "incident_agent" else "GENERATE_FINAL_REPORT"
            workflow_state["approval_needed"] = not request_human_approval(
                action_type,
                {"user_message": user_message},
            )
            workflow_state["approved"] = not workflow_state["approval_needed"]
            if workflow_state["approval_needed"]:
                workflow_state["agent_response"] = (
                    f"{route} is awaiting human approval before continuing."
                )
                workflow_state["conversation_history"].append(
                    {"role": "assistant", "content": workflow_state["agent_response"]}
                )
                return workflow_state

        try:
            if route == "alert_agent":
                workflow_state = alert_analysis_agent(workflow_state)
            elif route == "identity_agent":
                workflow_state = identity_agent(workflow_state)
            elif route == "endpoint_agent":
                workflow_state = endpoint_agent(workflow_state)
            elif route == "incident_agent":
                workflow_state = incident_agent(workflow_state)
            elif route == "reporting_agent":
                workflow_state = reporting_agent(workflow_state)
            else:
                workflow_state["agent_response"] = "No specialist matched the request."
        except Exception as exc:  # pragma: no cover - defensive error handling
            workflow_state["agent_response"] = f"Workflow error: {exc}"
            workflow_state["error_logs"] = str(exc)

        workflow_state["conversation_history"].append(
            {"role": "assistant", "content": workflow_state.get("agent_response", "")}
        )
        return workflow_state

    return run_workflow
