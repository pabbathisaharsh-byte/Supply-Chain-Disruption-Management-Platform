# app/tools/endpoint_tools.py
"""
Purpose: Tool & Integration Engineer (Team Member 2)
Role:
- Interfaces with the Mock Endpoint Protection System (EDR).
- Provides functions to look up device health, workstation status, and check for malware detections.
"""

# In-memory mock database of workstation assets and endpoint threat details
ENDPOINT_ASSETS_DATABASE = {
    "WS-900": {
        "device_name": "WS-900",
        "assigned_user": "jdoe",
        "os": "Windows 11 Enterprise",
        "edr_agent_status": "ACTIVE",
        "is_infected": True,
        "last_malware_detection": "Trojan.Win32.Generic",
        "last_seen": "2024-07-24T08:32:00Z",
        "firewall_active": True,
        "encryption_enabled": True,
        "antivirus_signature_version": "v1.409.2",
        "outbound_connections_count": 1450,
        "managed_device": True
    },
    "WS-550": {
        "device_name": "WS-550",
        "assigned_user": "unmanaged",
        "os": "macOS Sonoma",
        "edr_agent_status": "INACTIVE",
        "is_infected": False,
        "last_malware_detection": "None",
        "last_seen": "2024-07-24T11:58:00Z",
        "firewall_active": False,
        "encryption_enabled": False,
        "antivirus_signature_version": "v0.0.0",
        "outbound_connections_count": 120,
        "managed_device": False
    },
    "WS-202": {
        "device_name": "WS-202",
        "assigned_user": "developer1",
        "os": "Ubuntu 22.04 LTS",
        "edr_agent_status": "ACTIVE",
        "is_infected": True,
        "last_malware_detection": "Suspicious-Ransomware-Script",
        "last_seen": "2024-07-24T09:02:00Z",
        "firewall_active": True,
        "encryption_enabled": True,
        "antivirus_signature_version": "v1.409.2",
        "outbound_connections_count": 300,
        "managed_device": True
    }
}

def check_device_status(device_name):
    """
    Mock function to retrieve current EDR/Endpoint health and status.

    Args:
        device_name (str): Name of the endpoint (e.g., WS-900).

    Returns:
        dict: Device status, OS details, last check-in, and agent health state.
    """
    return ENDPOINT_ASSETS_DATABASE.get(device_name.upper())

def verify_device_health(device_name):
    """
    Checks if security policies are compliant (e.g., Firewall ON, Disk Encrypted).

    Args:
        device_name (str): Workstation or device identifier.

    Returns:
        dict: Health check indicators.
    """
    device = ENDPOINT_ASSETS_DATABASE.get(device_name.upper())
    if not device:
        return None
    return {
        "device_name": device["device_name"],
        "firewall_active": device["firewall_active"],
        "encryption_enabled": device["encryption_enabled"],
        "antivirus_signature_version": device["antivirus_signature_version"],
        "managed_device": device["managed_device"]
    }
