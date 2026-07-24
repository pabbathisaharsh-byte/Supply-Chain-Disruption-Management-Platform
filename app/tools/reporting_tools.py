# app/tools/reporting_tools.py
"""
Purpose: Tool & Integration Engineer (Team Member 2)
Role:
- Facilitates automated generation of investigation reports and summaries.
- Combines information retrieved across multiple specialist domains to format security writeups.
"""

def generate_investigation_report(incident_id, analyst_notes):
    """
    Mock function to draft a complete SOC analyst report.
    Requires Human-in-the-Loop validation before finalization.

    Args:
        incident_id (str): The incident target.
        analyst_notes (str): Additional context provided by the analyst or AI.

    Returns:
        dict: Generated report metadata and generated markdown body.
    """
    return {
        "report_id": "REP-8082",
        "incident_id": incident_id,
        "format": "Markdown",
        "content_summary": f"Investigation of Incident {incident_id}. Notes: {analyst_notes}",
        "generated_at": "2024-07-24T09:00:00Z"
    }

def summarize_security_alerts(alerts):
    """
    Uses LLM patterns or basic summarizers to group alerts.

    Args:
        alerts (list): List of security alerts.

    Returns:
        str: Concise textual summary.
    """
    return f"Summarized {len(alerts)} alerts. Primary systems affected: " + ", ".join(list(set(a['system'] for a in alerts)))
