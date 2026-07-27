# app/agents/specialists.py
"""
Purpose: Multi-Agent Engineer (Team Member 4)
Role:
- Implements specialized security agents that handle domain-specific workflows.
- These agents are designed to execute tools provided by the Tool & Integration Engineer and format replies.
"""

from app.tools.alert_tools import search_alerts, get_alert_details
from app.tools.identity_tools import check_login_history, search_user_activity
from app.tools.endpoint_tools import check_device_status, verify_device_health
from app.tools.incident_tools import create_security_incident, check_incident_status, escalate_incident, close_investigation
from app.tools.reporting_tools import generate_investigation_report, summarize_security_alerts
from app.tools.correlation_tools import correlate_events

def alert_analysis_agent(state):
    """
    Handles Security Alerts, Alert Severities, and Threat Summaries.
    Invokes alert search and details retrieval tools.
    """
    msg = state.get("user_message", "").lower()

    # Check if querying a specific alert
    if "alt-" in msg:
        import re
        match = re.search(r"alt-\d+", msg)
        if match:
            alert_id = match.group(0).upper()
            details = get_alert_details(alert_id)
            if details:
                state["agent_response"] = (
                    f"### [Alert Details] {alert_id}\n"
                    f"- **System:** {details['system']}\n"
                    f"- **Description:** {details['description']}\n"
                    f"- **Severity:** {details['severity']}\n"
                    f"- **Source Device:** {details['source_device']}\n"
                    f"- **Status:** {details['status']}"
                )
                return state

    # Default to search/list
    severity_filter = None
    for sev in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]:
        if sev.lower() in msg:
            severity_filter = sev
            break

    alerts = search_alerts(severity=severity_filter)
    summary = summarize_security_alerts(alerts)

    response_text = f"### SIEM & Firewall Alerts Found\n{summary}\n\n"
    for a in alerts[:5]:
        response_text += f"- **{a['alert_id']}** ({a['severity']}): {a['description']} on *{a['source_device']}*\n"

    state["agent_response"] = response_text
    return state

def endpoint_agent(state):
    """
    Handles Device Health, Malware Detections, and EDR Statuses.
    Invokes endpoint status and EDR health tools.
    """
    msg = state.get("user_message", "").lower()

    # Identify target workstation/device
    device_target = "WS-900" # default
    if "ws-550" in msg:
        device_target = "WS-550"
    elif "ws-202" in msg:
        device_target = "WS-202"

    status = check_device_status(device_target)
    if not status:
        state["agent_response"] = f"Error: Endpoint asset '{device_target}' was not found in the EDR database."
        return state

    health = verify_device_health(device_target)

    state["agent_response"] = (
        f"### Endpoint Security Status: {device_target}\n"
        f"- **Assigned User:** {status['assigned_user']}\n"
        f"- **Operating System:** {status['os']}\n"
        f"- **EDR Agent Status:** {status['edr_agent_status']}\n"
        f"- **Is Malware Detected?:** {'YES' if status['is_infected'] else 'NO'}\n"
        f"- **Last Malware Threat:** {status['last_malware_detection']}\n"
        f"- **Managed Device?:** {'YES' if status['managed_device'] else 'NO'}\n"
        f"- **Local Firewall Active?:** {'YES' if health['firewall_active'] else 'NO'}\n"
        f"- **Disk Encrypted?:** {'YES' if health['encryption_enabled'] else 'NO'}"
    )
    return state

def identity_agent(state):
    """
    Handles Logins, Failed Attempts, User Activities, and Authentication logs.
    """
    msg = state.get("user_message", "").lower()

    username = "jdoe"
    if "admin_ops" in msg:
        username = "admin_ops"
    elif "developer1" in msg:
        username = "developer1"

    history = check_login_history(username)
    activities = search_user_activity(username)

    response_text = f"### Identity and IAM Profiling: {username}\n"
    response_text += "#### Recent Authentication Records:\n"
    for h in history[:3]:
        response_text += f"- {h['timestamp']}: Status: **{h['status']}** from {h['ip_address']} ({h['location']}) - *{h['details']}*\n"

    response_text += "\n#### Recent Access & User Actions:\n"
    if activities:
        for act in activities:
            response_text += f"- {act['timestamp']}: Action: **{act['action']}** on {act['resource']} (Status: {act['status']})\n"
    else:
        response_text += "- No abnormal resource activities recorded.\n"

    state["agent_response"] = response_text
    return state

def incident_agent(state):
    """
    Handles Incident Ticket Creation, Escalations, and Status queries.
    Demands Human-in-the-Loop check before critical mutations.
    """
    msg = state.get("user_message", "").lower()

    if "create" in msg or "open" in msg:
        # Halt execution and request approval
        state["approval_needed"] = True
        state["approval_action"] = "CREATE_INCIDENT"
        state["approval_details"] = {
            "title": "Incident Creation Request",
            "description": "Create security incident based on security analyst session query.",
            "priority": "HIGH"
        }
        state["agent_response"] = "### Action Pending Confirmation\nThis action requires Human-in-the-loop authorization to prevent false-positive ticket generation."
        return state

    if "escalate" in msg:
        # Find target incident id
        import re
        match = re.search(r"inc-2024-\d+", msg)
        inc_id = match.group(0).upper() if match else "INC-2024-001"

        state["approval_needed"] = True
        state["approval_action"] = "ESCALATE_INCIDENT"
        state["approval_details"] = {
            "incident_id": inc_id,
            "reason": "Escalating incident to Tier 3 CIRT team due to advanced correlation signals."
        }
        state["agent_response"] = f"### Action Pending Confirmation\nEscalating incident **{inc_id}** requires Human-in-the-loop authorization."
        return state

    if "close" in msg:
        import re
        match = re.search(r"inc-2024-\d+", msg)
        inc_id = match.group(0).upper() if match else "INC-2024-001"

        state["approval_needed"] = True
        state["approval_action"] = "CLOSE_INVESTIGATION"
        state["approval_details"] = {
            "incident_id": inc_id
        }
        state["agent_response"] = f"### Action Pending Confirmation\nClosing investigation for incident **{inc_id}** requires Human-in-the-loop validation."
        return state

    # Default to status lookup
    import re
    match = re.search(r"inc-2024-\d+", msg)
    if match:
        inc_id = match.group(0).upper()
        status = check_incident_status(inc_id)
        if status:
            state["agent_response"] = (
                f"### Incident Status: {inc_id}\n"
                f"- **Title:** {status['title']}\n"
                f"- **Description:** {status['description']}\n"
                f"- **Priority:** {status['priority']}\n"
                f"- **Ticket Status:** {status['status']}\n"
                f"- **Assignee:** {status['assignee']}\n"
                f"- **Created At:** {status['created_at']}"
            )
            return state

    state["agent_response"] = "### Incident Management\nSpecify a ticket ID (e.g., INC-2024-001) or request to 'create incident' or 'escalate incident'."
    return state

def reporting_agent(state):
    """
    Handles Incident Timeline, Investigation Reports, Executive Summaries, and Correlation.
    Demands Human-in-the-Loop check before final report generation.
    """
    msg = state.get("user_message", "").lower()

    # Handle Phase 2 Correlation Scenarios
    if "correlate" in msg or "campaign" in msg or "threat hunting" in msg or "scenarios" in msg:
        campaigns = correlate_events()

        response_text = "### Phase 2 Event Correlation & Threat Hunting Insights\n"
        response_text += f"The AI Correlation Engine parsed active SIEM, IAM, and EDR logs and successfully matched **{len(campaigns)}** high-confidence multi-stage attack scenarios:\n\n"

        for c in campaigns:
            response_text += f"#### [{c['campaign_id']}] {c['scenario_name']} (Risk Score: **{c['risk_score']}/100**)\n"
            response_text += f"- **Entities Involved:** `{c['involved_entities']}`\n"
            response_text += "- **Correlated Evidence Trails:**\n"
            for ev in c["correlated_events"]:
                response_text += f"  - *{ev}*\n"
            response_text += f"- **Explainable AI Reasoning:** {c['explainable_reasoning']}\n"
            response_text += "- **Recommended Action Steps:**\n"
            for step in c["recommended_investigation_path"]:
                response_text += f"  - {step}\n"
            response_text += "\n---\n"

        state["agent_response"] = response_text
        return state

    if "report" in msg:
        import re
        match = re.search(r"inc-2024-\d+", msg)
        inc_id = match.group(0).upper() if match else "INC-2024-001"

        state["approval_needed"] = True
        state["approval_action"] = "GENERATE_FINAL_REPORT"
        state["approval_details"] = {
            "incident_id": inc_id,
            "notes": "Generated automatically based on correlated firewall outbound activities and endpoint Trojan logs."
        }
        state["agent_response"] = "### Action Pending Confirmation\nDrafting and dispatching the final incident report requires Human-in-the-loop authorization."
        return state

    state["agent_response"] = "### Reporting Agent\nYou can ask to 'generate report' for a specific ticket or ask to 'correlate events' to view Threat Hunting scenarios."
    return state
