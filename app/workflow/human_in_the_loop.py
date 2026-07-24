# app/workflow/human_in_the_loop.py
"""
Purpose: Agent Engineer (Team Member 3)
Role:
- Manages human confirmation workflows.
- Implements guardrails/gates that halt execution before performing destructive or critical actions:
  - Creating an Incident
  - Escalating an Incident
  - Marking an Alert as Critical
  - Closing an Investigation
  - Generating a Final Report
"""

def request_human_approval(action_type, details):
    """
    Halts execution and requests confirmation for sensitive actions.

    Args:
        action_type (str): Type of action requiring validation.
        details (dict): Context parameters for validation.

    Returns:
        bool: True if authorized, False otherwise.
    """
    critical_actions = [
        "CREATE_INCIDENT",
        "ESCALATE_INCIDENT",
        "MARK_ALERT_CRITICAL",
        "CLOSE_INVESTIGATION",
        "GENERATE_FINAL_REPORT"
    ]
    if action_type in critical_actions:
        # Prompting structural simulation or setting internal state to 'AWAITING_APPROVAL'
        return False  # Defaults to pending analyst consent
    return True
