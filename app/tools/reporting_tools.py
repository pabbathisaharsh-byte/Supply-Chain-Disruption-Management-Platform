# app/tools/reporting_tools.py
"""
Purpose: Tool & Integration Engineer (Team Member 2)
Role:
- Facilitates automated generation of investigation reports and summaries.
- Combines information retrieved across multiple specialist domains to format security writeups.
"""

REPORTS_DATABASE = []

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
    report_id = f"REP-{8080 + len(REPORTS_DATABASE) + 1}"
    report_body = f"""# SECURITY INCIDENT INVESTIGATION REPORT: {incident_id}
**Report ID:** {report_id}
**Classification:** HIGHLY CONFIDENTIAL
**Date Generated:** 2024-07-24T09:00:00Z

## Executive Summary
This document summarizes the timeline, threat indicators, and analyst findings related to Security Incident {incident_id}.

## Incident Artifacts and Timeline
- Automated discovery triggered cross-platform telemetry check.
- High-risk multi-stage correlation completed.

## Analyst Investigation Notes
{analyst_notes}

## Mitigation Recommendations
1. Revoke active tokens and rotate authentication credentials.
2. Quarantine affected workstations.
3. Apply black-hole firewall routing to remote malicious IPs.
"""
    new_report = {
        "report_id": report_id,
        "incident_id": incident_id,
        "format": "Markdown",
        "content_summary": f"Investigation of Incident {incident_id}. Notes: {analyst_notes}",
        "full_report": report_body,
        "generated_at": "2024-07-24T09:00:00Z"
    }
    REPORTS_DATABASE.append(new_report)
    return new_report

def summarize_security_alerts(alerts):
    """
    Uses LLM patterns or basic summarizers to group alerts.

    Args:
        alerts (list): List of security alerts.

    Returns:
        str: Concise textual summary.
    """
    if not alerts:
        return "No alerts to summarize."
    systems = list(set(a['system'] for a in alerts))
    return f"Summarized {len(alerts)} alert(s). Primary affected system(s): {', '.join(systems)}. Max severity of: {max(a['severity'] for a in alerts)}."
