# app/tools/incident_tools.py
"""
Purpose: Tool & Integration Engineer (Team Member 2)
Role:
- Interfaces with the Mock Incident Management System.
- Facilitates creating security incidents, updating their statuses, and handling escalations.
"""

def create_security_incident(title, description, priority="HIGH"):
    """
    Mock function to log an incident in the ticketing system.
    Requires Human-in-the-Loop validation before calling.

    Args:
        title (str): Title of the security ticket.
        description (str): Detailed context or findings.
        priority (str): Ticket priority (LOW, MEDIUM, HIGH, CRITICAL).

    Returns:
        dict: Created incident confirmation including Incident ID.
    """
    return {
        "incident_id": "INC-2024-9081",
        "title": title,
        "description": description,
        "priority": priority,
        "status": "CREATED",
        "assignee": "SOC Tier 2 Team",
        "created_at": "2024-07-24T08:45:00Z"
    }

def check_incident_status(incident_id):
    """
    Mock function to query current status of an incident.

    Args:
        incident_id (str): Incident ticket ID.

    Returns:
        dict: Incident progress update.
    """
    return {
        "incident_id": incident_id,
        "status": "INVESTIGATING",
        "priority": "HIGH",
        "comments": "Correlating with multiple outbound network events."
    }

def escalate_incident(incident_id, escalation_reason):
    """
    Escalates an incident to Tier 3 or CISO.
    Requires Human-in-the-Loop validation before calling.

    Args:
        incident_id (str): Incident ticket ID.
        escalation_reason (str): Justification for escalation.

    Returns:
        dict: Escalation result details.
    """
    return {
        "incident_id": incident_id,
        "escalation_status": "ESCALATED_TIER3",
        "reason": escalation_reason,
        "timestamp": "2024-07-24T08:50:00Z"
    }
