# app/tools/identity_tools.py
"""
Purpose: Tool & Integration Engineer (Team Member 2)
Role:
- Interfaces with the Mock Identity & Access Management (IAM) system.
- Provides utility functions to look up user login history, failed logins, and related user activity logs.
"""

# In-memory mock database of login history and system user activities
LOGINS_DATABASE = [
    {
        "username": "jdoe",
        "timestamp": "2024-07-24T08:00:00Z",
        "ip_address": "203.0.113.5",
        "location": "United States",
        "status": "FAILED",
        "details": "Incorrect password"
    },
    {
        "username": "jdoe",
        "timestamp": "2024-07-24T08:02:00Z",
        "ip_address": "203.0.113.5",
        "location": "United States",
        "status": "FAILED",
        "details": "Incorrect password"
    },
    {
        "username": "jdoe",
        "timestamp": "2024-07-24T08:05:00Z",
        "ip_address": "198.51.100.42",
        "location": "Unknown Country",
        "status": "SUCCESS",
        "details": "MFA Challenge Bypassed via Session Hijack"
    },
    {
        "username": "admin_ops",
        "timestamp": "2024-07-24T03:15:00Z",
        "ip_address": "198.51.100.12",
        "location": "Unknown Location",
        "status": "SUCCESS",
        "details": "Successful logon outside working hours"
    },
    {
        "username": "developer1",
        "timestamp": "2024-07-24T10:00:00Z",
        "ip_address": "10.0.5.21",
        "location": "Corporate HQ VPN",
        "status": "SUCCESS",
        "details": "Standard login"
    }
]

USER_ACTIVITIES_DATABASE = [
    {
        "username": "jdoe",
        "timestamp": "2024-07-24T08:10:00Z",
        "action": "ACCESS_SENSITIVE_REPOS",
        "resource": "GitHub Enterprise /SecureCodebase",
        "status": "SUCCESS"
    },
    {
        "username": "admin_ops",
        "timestamp": "2024-07-24T03:20:00Z",
        "action": "DUMP_ACTIVE_DIRECTORY",
        "resource": "Domain Controller DC-01",
        "status": "SUCCESS"
    },
    {
        "username": "developer1",
        "timestamp": "2024-07-24T11:00:00Z",
        "action": "GIT_PULL",
        "resource": "GitHub Enterprise /SecureCodebase",
        "status": "SUCCESS"
    }
]

def check_login_history(username=None):
    """
    Mock function to retrieve login logs from the Identity Management Platform.

    Args:
        username (str): The specific username to check.

    Returns:
        list: Login history records containing timestamp, location, success status, and IP.
    """
    if username:
        return [l for l in LOGINS_DATABASE if l["username"].lower() == username.lower()]
    return LOGINS_DATABASE

def search_user_activity(username):
    """
    Mock function to track user actions across systems during threat hunting.

    Args:
        username (str): The username to investigate.

    Returns:
        list: Activity details including source systems, resource accessed, and timestamps.
    """
    return [a for a in USER_ACTIVITIES_DATABASE if a["username"].lower() == username.lower()]
