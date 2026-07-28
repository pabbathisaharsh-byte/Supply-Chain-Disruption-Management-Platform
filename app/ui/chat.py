# app/ui/chat.py
"""
Purpose: AI Conversation Engineer (Team Member 1)
Role:
- Manages the Chat UI using Streamlit.
- Implements conversation memory and session-based history management to ensure a seamless analyst experience.
- Handles UI layouts and displays agent responses and correlation outputs to the SOC analyst.
- Displays human-in-the-loop validation prompts.
- Employs professional metrics, custom layout columns, tabs, and styled containers for a clean executive UI.
"""

import streamlit as st
from app.workflow.graph import execute_agent_workflow
from app.workflow.human_in_the_loop import handle_human_approval

def render_chat_interface():
    """
    Renders an enhanced, enterprise-grade Streamlit chat interface.
    Features real-time security telemetry, detailed system roles, sample prompt buttons,
    integrated human-in-the-loop validation boxes, and beautifully-formatted logs.
    """
    st.set_page_config(
        page_title="SecureOps AI - Advanced SOC Assistant",
        page_icon="🛡️",
        layout="wide"
    )

    # Custom CSS for modern styling
    st.markdown("""
        <style>
        .main {
            background-color: #0f172a;
            color: #f1f5f9;
        }
        .stSidebar {
            background-color: #1e293b !important;
        }
        .report-box {
            background-color: #1e293b;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #3b82f6;
            margin-bottom: 10px;
        }
        .metric-card {
            background-color: #1e293b;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #334155;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Top Header Banner
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1e3a8a, #0f172a); padding: 25px; border-radius: 12px; margin-bottom: 25px; border: 1px solid #2563eb;">
            <h1 style="color: #f8fafc; margin: 0; font-size: 2.2rem;">🛡️ SecureOps AI - Security Operations Assistant</h1>
            <p style="color: #94a3b8; margin: 8px 0 0 0; font-size: 1.05rem;">
                Autonomous Threat Hunting, Multi-Source Alert Correlation & Multi-Agent Incident Orchestration Engine
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Telemetry Panel (Executive Dashboard Metrics)
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown("""
            <div class="metric-card">
                <span style="color: #94a3b8; font-size: 0.85rem; font-weight: 600;">ACTIVE TELEMETRY SOURCES</span>
                <h3 style="color: #38bdf8; margin: 5px 0 0 0; font-size: 1.6rem;">4 Systems</h3>
                <span style="color: #10b981; font-size: 0.75rem;">SIEM, EDR, IAM, Tickets</span>
            </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown("""
            <div class="metric-card">
                <span style="color: #94a3b8; font-size: 0.85rem; font-weight: 600;">ACTIVE THREAT CAMPAIGNS</span>
                <h3 style="color: #ef4444; margin: 5px 0 0 0; font-size: 1.6rem;">5 Scenarios</h3>
                <span style="color: #f87171; font-size: 0.75rem;">Phase 2 Correlation Engine</span>
            </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown("""
            <div class="metric-card">
                <span style="color: #94a3b8; font-size: 0.85rem; font-weight: 600;">AGENT WORKFLOW ENGINE</span>
                <h3 style="color: #10b981; margin: 5px 0 0 0; font-size: 1.6rem;">LangGraph</h3>
                <span style="color: #34d399; font-size: 0.75rem;">Active Node Supervision</span>
            </div>
        """, unsafe_allow_html=True)
    with col_m4:
        st.markdown("""
            <div class="metric-card">
                <span style="color: #94a3b8; font-size: 0.85rem; font-weight: 600;">DEFAULT LLM CORE</span>
                <h3 style="color: #6366f1; margin: 5px 0 0 0; font-size: 1.6rem;">llama3.2</h3>
                <span style="color: #a5b4fc; font-size: 0.75rem;">Ollama local container</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Sidebar - Team Roles & Documentation
    with st.sidebar:
        st.markdown("<h2 style='color: #38bdf8;'>👥 SOC Consulting Team</h2>", unsafe_allow_html=True)
        st.write("Each module corresponds to a distinct consultant engineer role:")
        st.info(
            "1. **AI Conversation Engineer**\n"
            "   - Controls system prompts, UI elements, and memory state flow.\n"
            "2. **Tool & Integration Engineer**\n"
            "   - Built REST endpoints and JSON databases for SIEM, EDR, IAM.\n"
            "3. **Agent Engineer**\n"
            "   - Formulates LangGraph state workflows and human-in-the-loop locks.\n"
            "4. **Multi-Agent Engineer**\n"
            "   - Spearheads supervisor routing and specialist execution nodes."
        )
        st.divider()
        st.markdown("<h3 style='color: #a78bfa;'>💡 Quick Commands</h3>", unsafe_allow_html=True)
        st.write("Click on any of the query options to explore telemetry:")

        # Streamlit quick query buttons
        if st.button("🔍 Show SIEM Security Alerts"):
            st.session_state.prompt_triggered = "show security alerts"

        if st.button("💻 Inspect Workstation WS-900"):
            st.session_state.prompt_triggered = "investigate workstation WS-900 status"

        if st.button("🔑 Analyze jdoe Authentication Logins"):
            st.session_state.prompt_triggered = "check logins for jdoe"

        if st.button("🛰️ Correlate Multi-Stage Threat Campaigns"):
            st.session_state.prompt_triggered = "correlate events and find threat hunting campaigns"

        if st.button("🎫 Request to Create Security Incident"):
            st.session_state.prompt_triggered = "create security incident"

    # Initialize Session state and conversation histories
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "pending_approval" not in st.session_state:
        st.session_state.pending_approval = None

    # Main columns - Split into left panel (Interactive Chat) and right panel (Active Investigation Logs)
    col_chat, col_logs = st.columns([2, 1])

    with col_chat:
        st.subheader("💬 Active Analyst Workstation")

        # Render historical chat records in modern layout bubble containers
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Interactive Human-in-the-Loop approval box
        if st.session_state.pending_approval:
            app_act = st.session_state.pending_approval["action"]
            app_det = st.session_state.pending_approval["details"]

            st.markdown(f"""
                <div style="background-color: #2e1065; padding: 18px; border-radius: 10px; border: 1.5px solid #a78bfa; margin: 15px 0;">
                    <h4 style="color: #f5f3ff; margin-top:0;">⚠️ Authorization Gating Triggered: <code>{app_act}</code></h4>
                    <p style="color: #ddd6fe; font-size:0.9rem; margin-bottom:10px;">
                        The agent logic is attempting to execute a mutation. Please verify and confirm this action:
                    </p>
                </div>
            """, unsafe_allow_html=True)
            st.json(app_det)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Confirm & Execute", key="hitl_approve", use_container_width=True):
                    res = handle_human_approval(app_act, app_det, analyst_approved=True)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"### 🟢 Gated Action Executed\n{res['message']}\n\n**Payload Details:**\n`{res['payload']}`"
                    })
                    st.session_state.pending_approval = None
                    st.rerun()
            with col2:
                if st.button("❌ Terminate Action", key="hitl_deny", use_container_width=True):
                    res = handle_human_approval(app_act, app_det, analyst_approved=False)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"### 🔴 Gated Action Cancelled\n{res['message']}"
                    })
                    st.session_state.pending_approval = None
                    st.rerun()

    with col_logs:
        st.subheader("📋 Active Telemetry Logs")
        with st.container():
            st.markdown("""
                <div class="report-box">
                    <strong style="color: #10b981;">● SYSTEM HEALTH: COMPLIANT</strong><br>
                    <span style="font-size: 0.85rem; color: #94a3b8;">All local JSON databases loaded successfully. EDR agent reporting standard check-ins.</span>
                </div>
                <div class="report-box" style="border-left-color: #ef4444;">
                    <strong style="color: #ef4444;">● INCIDENTS QUEUED: 1</strong><br>
                    <span style="font-size: 0.85rem; color: #94a3b8;">INC-2024-101: Unapproved AD dump is marked OPEN. Assignee: SOC Tier 2.</span>
                </div>
                <div class="report-box" style="border-left-color: #f59e0b;">
                    <strong style="color: #f59e0b;">● PHASE 2 EVENT CORRELATION</strong><br>
                    <span style="font-size: 0.85rem; color: #94a3b8;">Matched 5 distinct scenarios representing multi-turn compromises, ransomware preparation, and privilege escalations.</span>
                </div>
            """, unsafe_allow_html=True)

    # Capture prompt from user or quick command buttons
    prompt = None
    if prompt_input := st.chat_input("Query SecureOps AI...", key="user_chat_input"):
        prompt = prompt_input
    elif "prompt_triggered" in st.session_state and st.session_state.prompt_triggered:
        prompt = st.session_state.prompt_triggered
        st.session_state.prompt_triggered = None  # Clear triggers

    if prompt:
        # Append and render user query
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Execute multi-agent workflow graph run
        state = execute_agent_workflow(prompt, st.session_state.messages[:-1])

        # If approval required, stash in session
        if state["approval_needed"]:
            st.session_state.pending_approval = {
                "action": state["approval_action"],
                "details": state["approval_details"]
            }

        # Append and render assistant response
        response_content = f"**[Routed Agent Node: {state['current_agent'].upper()}]**\n\n" + state["agent_response"]
        if state["error_logs"]:
            response_content += f"\n\n*⚠️ Developer Note: {state['error_logs']}*"

        st.session_state.messages.append({"role": "assistant", "content": response_content})
        st.rerun()

if __name__ == "__main__":
    render_chat_interface()
