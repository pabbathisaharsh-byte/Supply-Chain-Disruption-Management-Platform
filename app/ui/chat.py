# app/ui/chat.py
"""
Purpose: AI Conversation Engineer (Team Member 1)
Role:
- Manages the Chat UI using Streamlit.
- Implements conversation memory and session-based history management to ensure a seamless analyst experience.
- Handles UI layouts and displays agent responses and correlation outputs to the SOC analyst.
- Displays human-in-the-loop validation prompts.
"""

import streamlit as st
from app.workflow.graph import execute_agent_workflow
from app.workflow.human_in_the_loop import handle_human_approval

def render_chat_interface():
    """
    Renders the Streamlit chat user interface.
    Provides fields for security analysts to query the SOC Assistant and display responses,
    including detailed security alerts, endpoint statuses, and threat hunting insights.
    """
    st.set_page_config(page_title="SecureOps AI - SOC Assistant", layout="wide")

    st.title("🛡️ SecureOps AI - Security Operations Center (SOC) Assistant")
    st.write(
        "Welcome to the Unified Threat Hunting, Alert Correlation & Multi-Agent Investigation Platform. "
        "SecureOps AI streamlines operations across SIEM, Endpoint EDR, Identity Management, and Ticket systems."
    )

    # Left sidebar - Team roles & System Configuration
    with st.sidebar:
        st.subheader("👥 SOC Consulting Team Roles")
        st.info(
            "1. **AI Conversation Engineer**\n"
            "   - Controls System prompts & User Experience\n"
            "2. **Tool & Integration Engineer**\n"
            "   - Built REST integrations (SIEM, EDR, IAM, Tickets)\n"
            "3. **Agent Engineer**\n"
            "   - Formulates LangGraph and Human-in-the-loop flow\n"
            "4. **Multi-Agent Engineer**\n"
            "   - Supervisor & Specialist routing behaviors"
        )
        st.divider()
        st.subheader("💡 Sample Investigation Prompts")
        st.markdown(
            "- *'show security alerts'*\n"
            "- *'investigate workstation WS-900 status'*\n"
            "- *'check logins for jdoe'*\n"
            "- *'correlate events and find threat hunting campaigns'*\n"
            "- *'create incident'*\n"
            "- *'escalate incident INC-2024-001'*"
        )

    # Init Session history and Memory
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "pending_approval" not in st.session_state:
        st.session_state.pending_approval = None

    # Render previous conversation memory history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Human-in-the-Loop Approval workflow panel
    if st.session_state.pending_approval:
        app_act = st.session_state.pending_approval["action"]
        app_det = st.session_state.pending_approval["details"]

        st.warning(f"⚠️ **Authorization Needed**: Request to execute critical system action: `{app_act}`")
        st.json(app_det)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Approve & Execute Action"):
                # Execute gated tool
                res = handle_human_approval(app_act, app_det, analyst_approved=True)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"### 🟢 Gated Action Executed\n{res['message']}\n\n**Payload Details:**\n`{res['payload']}`"
                })
                st.session_state.pending_approval = None
                st.rerun()
        with col2:
            if st.button("❌ Deny Action"):
                res = handle_human_approval(app_act, app_det, analyst_approved=False)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"### 🔴 Gated Action Cancelled\n{res['message']}"
                })
                st.session_state.pending_approval = None
                st.rerun()

    # Chat User input interface
    if prompt := st.chat_input("Ask SecureOps AI... (e.g. 'show alerts', 'correlate events')"):
        # Append and render user query
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Execute multi-agent workflow graph run
        with st.spinner("Supervisor Agent evaluating query & routing to Specialist..."):
            state = execute_agent_workflow(prompt, st.session_state.messages)

        # If approval required, stash in session
        if state["approval_needed"]:
            st.session_state.pending_approval = {
                "action": state["approval_action"],
                "details": state["approval_details"]
            }

        # Append and render assistant response
        response_content = f"**[Routed Node: {state['current_agent'].upper()}]**\n\n" + state["agent_response"]
        if state["error_logs"]:
            response_content += f"\n\n*⚠️ Developer Note: {state['error_logs']}*"

        st.session_state.messages.append({"role": "assistant", "content": response_content})
        st.rerun()

if __name__ == "__main__":
    render_chat_interface()
