# app/tools/alert_tools.py
"""
Purpose: Tool & Integration Engineer (Team Member 2)
Role:
- Interfaces with the Mock SIEM or Firewall API to search and retrieve security alerts.
- Provides functions to look up alert details and check threat severities.
"""

# In-memory mock database of SIEM and Firewall alerts
ALERTS_DATABASE = [
    {
        "alert_id": "ALT-101",
        "system": "Firewall",
        "description": "High volume of outbound traffic detected to external IP 198.51.100.42",
        "severity": "HIGH",
        "status": "OPEN",
        "source_device": "WS-900",
        "dest_ip": "198.51.100.42",
        "timestamp": "2024-07-24T08:30:00Z"
    },
    {
        "alert_id": "ALT-102",
        "system": "Endpoint Protection",
        "description": "Suspicious Trojan.Win32.Generic binary executed",
        "severity": "HIGH",
        "status": "OPEN",
        "source_device": "WS-900",
        "dest_ip": "None",
        "timestamp": "2024-07-24T08:35:00Z"
    },
    {
        "alert_id": "ALT-103",
        "system": "Identity Management",
        "description": "Multiple failed logins followed by successful login from Unknown Country (198.51.100.42)",
        "severity": "MEDIUM",
        "status": "OPEN",
        "source_device": "Remote-IP-198.51.100.42",
        "dest_ip": "None",
        "timestamp": "2024-07-24T08:05:00Z"
    },
    {
        "alert_id": "ALT-104",
        "system": "Firewall",
        "description": "Outbound connection to known Tor exit node",
        "severity": "CRITICAL",
        "status": "OPEN",
        "source_device": "WS-550",
        "dest_ip": "192.0.2.11",
        "timestamp": "2024-07-24T12:00:00Z"
    },
    {
        "alert_id": "ALT-105",
        "system": "Identity Management",
        "description": "Privileged account activity outside normal working hours",
        "severity": "MEDIUM",
        "status": "OPEN",
        "source_device": "Admin-Portal",
        "dest_ip": "None",
        "timestamp": "2024-07-24T03:15:00Z"
    },
    {
        "alert_id": "ALT-106",
        "system": "Cloud Infrastructure",
        "description": "S3 Bucket permission updated to public access",
        "severity": "HIGH",
        "status": "OPEN",
        "source_device": "CloudConsole-Admin",
        "dest_ip": "None",
        "timestamp": "2024-07-24T14:20:00Z"
    },
    {
        "alert_id": "ALT-107",
        "system": "Cloud Infrastructure",
        "description": "Abnormal API volume usage on AWS CloudTrail",
        "severity": "MEDIUM",
        "status": "OPEN",
        "source_device": "CloudConsole-Admin",
        "dest_ip": "None",
        "timestamp": "2024-07-24T14:21:00Z"
    },
    {
        "alert_id": "ALT-108",
        "system": "Endpoint Protection",
        "description": "Suspicious PowerShell script attempting to stop shadow copies (VSS)",
        "severity": "LOW",
        "status": "OPEN",
        "source_device": "WS-202",
        "dest_ip": "None",
        "timestamp": "2024-07-24T09:00:00Z"
    },
    {
        "alert_id": "ALT-109",
        "system": "Endpoint Protection",
        "description": "Localized file encryption pattern matching Ransomware behavior",
        "severity": "LOW",
        "status": "OPEN",
        "source_device": "WS-202",
        "dest_ip": "None",
        "timestamp": "2024-07-24T09:05:00Z"
    }
]

def search_alerts(query=None, severity=None):
    """
    Mock function to search security alerts in the SIEM platform.

    Args:
        query (str): Optional query string to filter alerts.
        severity (str): Optional severity level (LOW, MEDIUM, HIGH, CRITICAL).

    Returns:
        list: A list of mock alert dictionaries containing ID, system, description, and timestamp.
    """
    results = ALERTS_DATABASE
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
    for alert in ALERTS_DATABASE:
        if alert["alert_id"].upper() == alert_id.upper():
            return alert
    return None

def update_alert_severity(alert_id, new_severity):
    """
    Simulates updating alert severity level. Requires Human-in-the-Loop validation if marking as CRITICAL.
    """
    for alert in ALERTS_DATABASE:
        if alert["alert_id"].upper() == alert_id.upper():
            alert["severity"] = new_severity.upper()
            return {"alert_id": alert_id, "status": "UPDATED", "severity": alert["severity"]}
    return None
