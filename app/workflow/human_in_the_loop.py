# app/workflow/human_in_the_loop.py
"""
Purpose: Agent Engineer (Team Member 3)
Role:
- Manages human confirmation workflows.
- Implements guardrails/gates that halt execution before performing destructive or critical actions:
  - Creating an Incident
  - Escalating an Incident
  - Marking an Alert as Critical
  - Closing an Investigation
  - Generating a Final Report
"""

from app.tools.incident_tools import create_security_incident, escalate_incident, close_investigation
from app.tools.reporting_tools import generate_investigation_report
from app.tools.alert_tools import update_alert_severity

def handle_human_approval(action_type, details, analyst_approved=True):
    """
    Acts as a gating filter for sensitive mutations.
    Executes the underlying tool only if analyst_approved is True.

    Args:
        action_type (str): Type of critical mutation.
        details (dict): Metadata payload.
        analyst_approved (bool): Validation confirmation status from the analyst.

    Returns:
        dict: Success details of execution, or failure log.
    """
    if not analyst_approved:
        return {
            "status": "DENIED",
            "message": f"Action '{action_type}' was explicitly denied by the security analyst."
        }

    try:
        if action_type == "CREATE_INCIDENT":
            title = details.get("title", "New Incident")
            desc = details.get("description", "No details")
            pri = details.get("priority", "HIGH")
            result = create_security_incident(title, desc, pri)
            return {
                "status": "APPROVED_AND_EXECUTED",
                "message": f"Incident successfully created with ID {result['incident_id']}.",
                "payload": result
            }

        elif action_type == "ESCALATE_INCIDENT":
            inc_id = details.get("incident_id")
            reason = details.get("reason", "No reason provided")
            result = escalate_incident(inc_id, reason)
            return {
                "status": "APPROVED_AND_EXECUTED",
                "message": f"Incident {inc_id} was escalated successfully to Tier 3 CIRT.",
                "payload": result
            }

        elif action_type == "MARK_ALERT_CRITICAL":
            alert_id = details.get("alert_id")
            result = update_alert_severity(alert_id, "CRITICAL")
            return {
                "status": "APPROVED_AND_EXECUTED",
                "message": f"Alert {alert_id} severity updated to CRITICAL.",
                "payload": result
            }

        elif action_type == "CLOSE_INVESTIGATION":
            inc_id = details.get("incident_id")
            result = close_investigation(inc_id)
            return {
                "status": "APPROVED_AND_EXECUTED",
                "message": f"Investigation for incident {inc_id} closed successfully.",
                "payload": result
            }

        elif action_type == "GENERATE_FINAL_REPORT":
            inc_id = details.get("incident_id")
            notes = details.get("notes", "")
            result = generate_investigation_report(inc_id, notes)
            return {
                "status": "APPROVED_AND_EXECUTED",
                "message": f"Final report generated successfully. ID: {result['report_id']}",
                "payload": result
            }

    except Exception as e:
        return {
            "status": "EXECUTION_ERROR",
            "message": f"Failed to execute gated action {action_type}: {str(e)}"
        }

    return {
        "status": "ERROR",
        "message": f"Unknown gated action type: {action_type}"
    }
