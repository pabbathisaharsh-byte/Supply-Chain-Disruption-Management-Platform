# app/tools/identity_tools.py
"""
Purpose: Tool & Integration Engineer (Team Member 2)
Role:
- Interfaces with the Mock Identity & Access Management (IAM) system.
- Provides utility functions to look up user login history, failed logins, and related user activity logs.
"""

def check_login_history(username=None):
    """
    Mock function to retrieve login logs from the Identity Management Platform.

    Args:
        username (str): The specific username to check.

    Returns:
        list: Login history records containing timestamp, location, success status, and IP.
    """
    return [
        {
            "username": username or "jdoe",
            "timestamp": "2024-07-24T08:00:00Z",
            "ip_address": "203.0.113.5",
            "location": "United States",
            "status": "FAILED",
            "details": "Incorrect password"
        },
        {
            "username": username or "jdoe",
            "timestamp": "2024-07-24T08:05:00Z",
            "ip_address": "198.51.100.42",
            "location": "Unknown Country",
            "status": "SUCCESS",
            "details": "Successful authentications after repeated failures"
        }
    ]

def search_user_activity(username):
    """
    Mock function to track user actions across systems during threat hunting.

    Args:
        username (str): The username to investigate.

    Returns:
        list: Activity details including source systems, resource accessed, and timestamps.
    """
    return [
        {
            "username": username,
            "timestamp": "2024-07-24T08:10:00Z",
            "action": "ACCESS_SENSITIVE_REPOS",
            "resource": "GitHub Enterprise /SecureCodebase",
            "status": "SUCCESS"
        }
    ]
