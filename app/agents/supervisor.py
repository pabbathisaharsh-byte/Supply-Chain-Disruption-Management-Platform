# app/agents/supervisor.py
"""
Purpose: Multi-Agent Engineer (Team Member 4)
Role:
- Acts as the central router (Supervisor Agent) receiving every security request.
- Uses prompt engineering and routing logic to delegate the analyst's request to specialized agents.
- Orchestrates multi-agent transitions within the LangGraph state machine.
"""

def route_request(state):
    """
    Evaluates current state context and routes the query to the correct specialist node.

    Args:
        state (dict): The shared graph state.

    Returns:
        str: The name of the next specialist node to invoke ('alert_agent', 'identity_agent', etc.)
    """
    user_message = state.get("user_message", "").lower()

    # Check for correlation or threat hunting requests first
    if "correlate" in user_message or "campaign" in user_message or "threat hunting" in user_message or "scenarios" in user_message:
        return "reporting_agent" # Reporting agent handles scenario layouts

    # Check for specific tool requests
    if "device" in user_message or "endpoint" in user_message or "malware" in user_message or "edr" in user_message or "workstation" in user_message:
        return "endpoint_agent"
    elif "alert" in user_message or "siem" in user_message or "firewall" in user_message:
        return "alert_agent"
    elif "login" in user_message or "failed attempt" in user_message or "user activity" in user_message or "auth" in user_message:
        return "identity_agent"
    elif "incident" in user_message or "escalate" in user_message or "ticket" in user_message:
        return "incident_agent"
    elif "report" in user_message or "summary" in user_message or "executive summary" in user_message:
        return "reporting_agent"

    return "alert_agent"  # Default fallback
