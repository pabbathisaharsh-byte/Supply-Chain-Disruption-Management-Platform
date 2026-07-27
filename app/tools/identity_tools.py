# app/tools/identity_tools.py
"""
Purpose: Tool & Integration Engineer (Team Member 2)
Role:
- Interfaces with the Mock Identity & Access Management (IAM) system.
- Provides utility functions to look up user login history, failed logins, and related user activity logs.
- Reads logins and user activities dynamically from local JSON files.
"""

import os
import json

LOGINS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "logins.json")
ACTIVITIES_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "user_activities.json")

def _load_logins():
    if not os.path.exists(LOGINS_FILE):
        return []
    with open(LOGINS_FILE, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return []

def _load_activities():
    if not os.path.exists(ACTIVITIES_FILE):
        return []
    with open(ACTIVITIES_FILE, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return []

def check_login_history(username=None):
    """
    Mock function to retrieve login logs from the Identity Management Platform.

    Args:
        username (str): The specific username to check.

    Returns:
        list: Login history records containing timestamp, location, success status, and IP.
    """
    logins = _load_logins()
    if username:
        return [l for l in logins if l["username"].lower() == username.lower()]
    return logins

def search_user_activity(username):
    """
    Mock function to track user actions across systems during threat hunting.

    Args:
        username (str): The username to investigate.

    Returns:
        list: Activity details including source systems, resource accessed, and timestamps.
    """
    activities = _load_activities()
    if username:
        return [a for a in activities if a["username"].lower() == username.lower()]
    return activities

def check_user_exists(username):
    """
    Checks if there are any login logs or user activity files tracking this username.
    """
    username_lower = username.lower()
    logins = _load_logins()
    for l in logins:
        if l["username"].lower() == username_lower:
            return True
    activities = _load_activities()
    for a in activities:
        if a["username"].lower() == username_lower:
            return True
    return False
