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
from app.workflow.graph import execute_agent_workflow
from app.workflow.human_in_the_loop import handle_human_approval

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
        self.assertEqual(history[2]["status"], "SUCCESS")

    def test_endpoint_tools(self):
        status = check_device_status("WS-900")
        self.assertTrue(status["is_infected"])

    def test_correlation_tools(self):
        correlation = correlate_events([])
        self.assertIsInstance(correlation, list)
        self.assertEqual(len(correlation), 5) # Assert exactly 5 distinct scenarios
        self.assertEqual(correlation[0]["campaign_id"], "CAMP-01")
        self.assertGreater(correlation[0]["risk_score"], 90)

    def test_supervisor_routing(self):
        state_alerts = {"user_message": "Can you check security alerts for severity levels?"}
        route = route_request(state_alerts)
        self.assertEqual(route, "alert_agent")

        state_identity = {"user_message": "check login activities of user jdoe"}
        route = route_request(state_identity)
        self.assertEqual(route, "identity_agent")

    def test_workflow_execution_and_routing(self):
        # Assert workflow maps correctly and yields formatted responses
        res = execute_agent_workflow("Show active security alerts")
        self.assertEqual(res["current_agent"], "alert_agent")
        self.assertIn("ALT-101", res["agent_response"])

        res_ep = execute_agent_workflow("Verify workstation WS-900 status details")
        self.assertEqual(res_ep["current_agent"], "endpoint_agent")
        self.assertIn("malware", res_ep["agent_response"].lower())

    def test_human_in_the_loop_approvals(self):
        # Request incident creation triggers HITL
        res = execute_agent_workflow("Open a security incident ticket")
        self.assertTrue(res["approval_needed"])
        self.assertEqual(res["approval_action"], "CREATE_INCIDENT")

        # Handle approved action execution
        details = res["approval_details"]
        exec_res = handle_human_approval("CREATE_INCIDENT", details, analyst_approved=True)
        self.assertEqual(exec_res["status"], "APPROVED_AND_EXECUTED")
        self.assertIn("INC-2024-", exec_res["message"])

        # Handle denied action execution
        exec_res_deny = handle_human_approval("CREATE_INCIDENT", details, analyst_approved=False)
        self.assertEqual(exec_res_deny["status"], "DENIED")

if __name__ == "__main__":
    unittest.main()
