# app/tools/incident_tools.py
"""
Purpose: Tool & Integration Engineer (Team Member 2)
Role:
- Interfaces with the Mock Incident Management System.
- Facilitates creating security incidents, updating their statuses, and handling escalations.
- Reads and mutates incidents database inside 'app/data/incidents.json'.
"""

import os
import json

INCIDENTS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "incidents.json")

def _load_incidents():
    if not os.path.exists(INCIDENTS_FILE):
        return []
    with open(INCIDENTS_FILE, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return []

def _save_incidents(incidents):
    with open(INCIDENTS_FILE, "w") as f:
        json.dump(incidents, f, indent=4)

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
    incidents = _load_incidents()
    incident_id = f"INC-2024-{100 + len(incidents) + 1}"
    new_ticket = {
        "incident_id": incident_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "OPEN",
        "assignee": "SOC Tier 2 Team",
        "created_at": "2024-07-24T08:45:00Z"
    }
    incidents.append(new_ticket)
    _save_incidents(incidents)
    return new_ticket

def check_incident_status(incident_id):
    """
    Mock function to query current status of an incident.

    Args:
        incident_id (str): Incident ticket ID.

    Returns:
        dict: Incident progress update or None if not found.
    """
    incidents = _load_incidents()
    for inc in incidents:
        if inc["incident_id"].upper() == incident_id.upper():
            return inc
    return None

def escalate_incident(incident_id, escalation_reason):
    """
    Escalates an incident to Tier 3 or CISO.
    Requires Human-in-the-Loop validation before calling.

    Args:
        incident_id (str): Incident ticket ID.
        escalation_reason (str): Justification for escalation.

    Returns:
        dict: Escalation result details or None if not found.
    """
    incidents = _load_incidents()
    for inc in incidents:
        if inc["incident_id"].upper() == incident_id.upper():
            inc["priority"] = "CRITICAL"
            inc["assignee"] = "SOC Tier 3 / CIRT Team"
            _save_incidents(incidents)
            return {
                "incident_id": incident_id,
                "escalation_status": "ESCALATED_TIER3",
                "reason": escalation_reason,
                "timestamp": "2024-07-24T08:50:00Z",
                "current_assignee": inc["assignee"]
            }
    return None

def close_investigation(incident_id):
    """
    Closes the investigation and updates the ticket status.
    Requires Human-in-the-Loop validation.
    """
    incidents = _load_incidents()
    for inc in incidents:
        if inc["incident_id"].upper() == incident_id.upper():
            inc["status"] = "CLOSED"
            _save_incidents(incidents)
            return {"incident_id": incident_id, "status": "CLOSED", "closed_at": "2024-07-24T09:15:00Z"}
    return None
