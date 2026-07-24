# app/tools/correlation_tools.py
"""
Purpose: Phase 2 Client Enhancement (Threat Hunting & Correlation)
Role:
- Correlates security alerts and events across different enterprise systems (SIEM, EDR, IAM, Threat Intel).
- Groups related observations into a unified investigation campaign.
- Computes priority/risk scoring and outputs explainable AI reasons behind the correlation.
"""

def correlate_events(events_list):
    """
    Correlates seemingly unrelated events across time, users, devices, and network IPs.

    Args:
        events_list (list): Raw list of alerts and user logs across multiple directories.

    Returns:
        dict: Correlated threat hunting campaign(s) featuring:
          - group_id
          - scenario_match (e.g. credential compromise, multi-stage malware)
          - involved_entities (devices, users, IPs)
          - risk_score (0-100)
          - explainable_reasoning (Why are these correlated?)
          - recommended_investigation_path
    """
    # Demonstration of mock correlation logic for a multi-stage attack:
    # 1. Multiple failed logins followed by a successful login from a new country.
    # 2. Malware detection on an endpoint followed by unusual outbound network traffic.
    return {
        "campaign_id": "CAMP-001",
        "scenario": "Compromised Credentials & Host-Based Malware Outbreak",
        "risk_score": 92,
        "correlated_events": [
            "ALT-101 (Firewall outbound traffic)",
            "ALT-102 (Endpoint malware infection)",
            "IAM-FailedLogins-jdoe"
        ],
        "explainable_reasoning": (
            "User 'jdoe' triggered multiple failed login attempts from a domestic IP, followed by "
            "a successful authentication from a foreign IP (198.51.100.42). Minutes later, workstation "
            "WS-900 (assigned to jdoe) downloaded a Trojan threat, and subsequently initiated high-volume "
            "outbound network traffic to the foreign IP. This strongly correlates a credential compromise "
            "leading to host-based infection and malicious command-and-control communication."
        ),
        "recommended_investigation_path": [
            "Isolate workstation WS-900 immediately via EDR tools.",
            "Revoke sessions and reset credentials for user account 'jdoe'.",
            "Block IP address 198.51.100.42 on the corporate firewall."
        ]
    }
