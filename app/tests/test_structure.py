# app/tests/test_structure.py
"""
Purpose: Testing (All Members)
Role:
- Basic structural tests ensuring that modules, tools, and agents are properly structured, mock data outputs are schema-compliant, and routing functions operate without syntax crashes.
"""

import unittest
from app.tools.alert_tools import search_alerts, get_alert_details
from app.tools.identity_tools import check_login_history, search_user_activity
from app.tools.endpoint_tools import check_device_status, verify_device_health
from app.tools.correlation_tools import correlate_events
from app.agents.supervisor import route_request

class TestSecureOpsStructure(unittest.TestCase):

    def test_alert_tools(self):
        alerts = search_alerts()
        self.assertIsInstance(alerts, list)
        self.assertGreater(len(alerts), 0)
        self.assertEqual(alerts[0]["alert_id"], "ALT-101")

        details = get_alert_details("ALT-101")
        self.assertEqual(details["severity"], "HIGH")

    def test_identity_tools(self):
        history = check_login_history("jdoe")
        self.assertGreater(len(history), 0)
        self.assertEqual(history[1]["status"], "SUCCESS")

    def test_endpoint_tools(self):
        status = check_device_status("WS-900")
        self.assertTrue(status["is_infected"])

    def test_correlation_tools(self):
        correlation = correlate_events([])
        self.assertIn("campaign_id", correlation)
        self.assertEqual(correlation["campaign_id"], "CAMP-001")
        self.assertGreater(correlation["risk_score"], 90)

    def test_supervisor_routing(self):
        state_alerts = {"user_message": "Can you check security alerts for severity levels?"}
        route = route_request(state_alerts)
        self.assertEqual(route, "alert_agent")

        state_identity = {"user_message": "check login activities of user jdoe"}
        route = route_request(state_identity)
        self.assertEqual(route, "identity_agent")

if __name__ == "__main__":
    unittest.main()
