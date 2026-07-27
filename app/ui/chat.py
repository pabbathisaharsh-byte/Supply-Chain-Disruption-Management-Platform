# app/ui/chat.py
"""
Purpose: AI Conversation Engineer (Team Member 1)
Role:
- Manages the Chat UI using Streamlit or similar frameworks.
- Implements conversation memory and session-based history management to ensure a seamless analyst experience.
- Handles UI layouts and displays agent responses and correlation outputs to the SOC analyst.
- Displays human-in-the-loop validation prompts.
"""

try:
    import streamlit as st
except ImportError:  # pragma: no cover - optional dependency for local execution
    st = None

from app.workflow.graph import build_workflow_graph


def manage_session_history(history=None):
    """
    Manages state, history, and memory across multiple turns in a user's session.
    Retrieves previous alerts or actions to prevent context loss.
    """
    if history is None:
        return []

    if not isinstance(history, list):
        return []

    clean_history = []
    for item in history:
        if isinstance(item, dict):
            clean_history.append(item)
    return clean_history


def render_chat_interface():
    """
    Renders the Streamlit chat user interface.
    Provides fields for security analysts to query the SOC Assistant and display responses,
    including detailed security alerts, endpoint statuses, and threat hunting insights.
    """
    workflow_runner = build_workflow_graph()

    if st is None:
        render_console_interface(workflow_runner)
        return

    st.set_page_config(page_title="SecureOps AI", page_icon="🛡️")
    st.title("SecureOps AI SOC Assistant")
    st.caption("Ask about alerts, endpoints, identities, incidents, or reports.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "workflow_runner" not in st.session_state:
        st.session_state.workflow_runner = workflow_runner

    for message in manage_session_history(st.session_state.messages):
        with st.chat_message(message.get("role", "assistant")):
            st.markdown(message.get("content", ""))

    prompt = st.chat_input("Ask the SOC assistant...")
    if prompt:
        state = st.session_state.workflow_runner(
            {
                "user_message": prompt,
                "conversation_history": manage_session_history(st.session_state.messages),
            }
        )
        st.session_state.messages = manage_session_history(state.get("conversation_history", []))


def render_console_interface(workflow_runner):
    """Provides a lightweight console fallback when Streamlit is unavailable."""
    print("SecureOps AI console mode. Type 'exit' to quit.")
    history = []

    while True:
        try:
            user_input = input("You: ").strip()
        except EOFError:
            break

        if not user_input or user_input.lower() in {"exit", "quit"}:
            break

        state = workflow_runner({"user_message": user_input, "conversation_history": history})
        history = manage_session_history(state.get("conversation_history", []))
        print(f"Assistant: {state.get('agent_response', '')}")
