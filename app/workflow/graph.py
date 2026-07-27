# app/workflow/graph.py
"""
Purpose: Agent Engineer (Team Member 3)
Role:
- Formulates the LangGraph state machine workflow.
- Defines state management, edge routers, and agent nodes.
- Integrates the supervisor agent and sub-agents into a unified reactive graph.
"""

from app.agents.supervisor import route_request
from app.agents.specialists import (
    alert_analysis_agent,
    endpoint_agent,
    identity_agent,
    incident_agent,
    reporting_agent
)

# Shared graph state dictionary format
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
    approval_action: str
    approval_details: dict
    approved: bool
    error_logs: str

def execute_agent_workflow(user_message, history=None):
    """
    Executes a structured multi-agent run.
    Uses the Supervisor Agent to determine the target agent, runs the selected specialist node,
    and returns the updated state dictionary.

    Args:
        user_message (str): The security analyst's query.
        history (list): List of past message turn dictionaries.

    Returns:
        dict: The final workflow output state dictionary.
    """
    # Initialize State
    state = {
        "user_message": user_message,
        "conversation_history": history or [],
        "current_agent": "supervisor",
        "agent_response": "",
        "approval_needed": False,
        "approval_action": "",
        "approval_details": {},
        "approved": False,
        "error_logs": ""
    }

    try:
        # 1. Supervisor Agent Routing Phase
        target_agent = route_request(state)
        state["current_agent"] = target_agent

        # 2. Specialist Execution Node Phase
        if target_agent == "alert_agent":
            state = alert_analysis_agent(state)
        elif target_agent == "endpoint_agent":
            state = endpoint_agent(state)
        elif target_agent == "identity_agent":
            state = identity_agent(state)
        elif target_agent == "incident_agent":
            state = incident_agent(state)
        elif target_agent == "reporting_agent":
            state = reporting_agent(state)
        else:
            state["error_logs"] = f"Unknown target specialist routing: {target_agent}"
            state = alert_analysis_agent(state)

    except Exception as e:
        state["error_logs"] = f"Runtime error in graph node execution: {str(e)}"
        state["agent_response"] = "An error occurred while routing or processing your request. Please check supervisor logs."

    return state
