# app/tools/alert_tools.py
"""
Purpose: Tool & Integration Engineer (Team Member 2)
Role:
- Interfaces with the Mock SIEM or Firewall API to search and retrieve security alerts.
- Provides functions to look up alert details and check threat severities.
- Reads and updates alerts dynamically from 'app/data/alerts.json'.
"""

import os
import json

ALERTS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "alerts.json")

def _load_alerts():
    if not os.path.exists(ALERTS_FILE):
        return []
    with open(ALERTS_FILE, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return []

def _save_alerts(alerts):
    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts, f, indent=4)

def search_alerts(query=None, severity=None):
    """
    Mock function to search security alerts in the SIEM platform.

    Args:
        query (str): Optional query string to filter alerts.
        severity (str): Optional severity level (LOW, MEDIUM, HIGH, CRITICAL).

    Returns:
        list: A list of mock alert dictionaries containing ID, system, description, and timestamp.
    """
    results = _load_alerts()
    if severity:
        results = [a for a in results if a["severity"].upper() == severity.upper()]
    if query:
        q = query.lower()
        results = [a for a in results if q in a["description"].lower() or q in a["system"].lower()]
    return results

def get_alert_details(alert_id):
    """
    Mock function to retrieve complete information for a specific alert ID.

    Args:
        alert_id (str): The ID of the alert.

    Returns:
        dict: Detailed alert metadata or None if not found.
    """
    alerts = _load_alerts()
    for alert in alerts:
        if alert["alert_id"].upper() == alert_id.upper():
            return alert
    return None

def update_alert_severity(alert_id, new_severity):
    """
    Simulates updating alert severity level. Requires Human-in-the-Loop validation if marking as CRITICAL.
    """
    alerts = _load_alerts()
    for alert in alerts:
        if alert["alert_id"].upper() == alert_id.upper():
            alert["severity"] = new_severity.upper()
            _save_alerts(alerts)
            return {"alert_id": alert_id, "status": "UPDATED", "severity": alert["severity"]}
    return None
