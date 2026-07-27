# app/tools/endpoint_tools.py
"""
Purpose: Tool & Integration Engineer (Team Member 2)
Role:
- Interfaces with the Mock Endpoint Protection System (EDR).
- Provides functions to look up device health, workstation status, and check for malware detections.
- Reads endpoints dynamically from 'app/data/endpoint_assets.json'.
"""

import os
import json

ENDPOINTS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "endpoint_assets.json")

def _load_endpoints():
    if not os.path.exists(ENDPOINTS_FILE):
        return {}
    with open(ENDPOINTS_FILE, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return {}

def check_device_status(device_name):
    """
    Mock function to retrieve current EDR/Endpoint health and status.

    Args:
        device_name (str): Name of the endpoint (e.g., WS-900).

    Returns:
        dict: Device status, OS details, last check-in, and agent health state.
    """
    endpoints = _load_endpoints()
    # Support case-insensitive key lookup
    for key, value in endpoints.items():
        if key.upper() == device_name.upper():
            return value
    return None

def verify_device_health(device_name):
    """
    Checks if security policies are compliant (e.g., Firewall ON, Disk Encrypted).

    Args:
        device_name (str): Workstation or device identifier.

    Returns:
        dict: Health check indicators.
    """
    device = check_device_status(device_name)
    if not device:
        return None
    return {
        "device_name": device["device_name"],
        "firewall_active": device["firewall_active"],
        "encryption_enabled": device["encryption_enabled"],
        "antivirus_signature_version": device["antivirus_signature_version"],
        "managed_device": device["managed_device"]
    }
