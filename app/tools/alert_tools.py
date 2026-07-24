# app/tools/alert_tools.py
"""
Purpose: Tool & Integration Engineer (Team Member 2)
Role:
- Interfaces with the Mock SIEM or Firewall API to search and retrieve security alerts.
- Provides functions to look up alert details and check threat severities.
"""

def search_alerts(query=None, severity=None):
    """
    Mock function to search security alerts in the SIEM platform.

    Args:
        query (str): Optional query string to filter alerts.
        severity (str): Optional severity level (LOW, MEDIUM, HIGH, CRITICAL).

    Returns:
        list: A list of mock alert dictionaries containing ID, system, description, and timestamp.
    """
    return [
        {
            "alert_id": "ALT-101",
            "system": "Firewall",
            "description": "Suspicious outbound traffic detected to external IP 198.51.100.42",
            "severity": "HIGH",
            "timestamp": "2024-07-24T08:30:00Z"
        },
        {
            "alert_id": "ALT-102",
            "system": "Endpoint Protection",
            "description": "Malware file signature detected on Workstation WS-900",
            "severity": "HIGH",
            "timestamp": "2024-07-24T08:35:00Z"
        }
    ]

def get_alert_details(alert_id):
    """
    Mock function to retrieve complete information for a specific alert ID.

    Args:
        alert_id (str): The ID of the alert.

    Returns:
        dict: Detailed alert metadata.
    """
    return {
        "alert_id": alert_id,
        "system": "Firewall Monitoring",
        "description": "Suspicious outbound traffic to IP 198.51.100.42",
        "severity": "HIGH",
        "status": "OPEN",
        "dest_ip": "198.51.100.42",
        "source_device": "WS-900",
        "timestamp": "2024-07-24T08:30:00Z"
    }
