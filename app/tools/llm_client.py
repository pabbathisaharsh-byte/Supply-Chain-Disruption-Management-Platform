from app.config import LLM_MODEL, LLM_TEMPERATURE

try:
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage
    _LANGCHAIN_AVAILABLE = True
except Exception:
    _LANGCHAIN_AVAILABLE = False


def _llm_available() -> bool:
    return _LANGCHAIN_AVAILABLE


def generate_response(system_prompt: str, user_prompt: str, model_name: str | None = None) -> str:
    """Generate an LLM response using the configured model and a system prompt.

    Falls back to a domain-aware templated greeting if the LLM environment is unavailable.
    """
    if model_name is None:
        model_name = LLM_MODEL

    if _llm_available():
        try:
            messages = [
                SystemMessage(content=system_prompt.strip()),
                HumanMessage(content=user_prompt.strip())
            ]
            llm = ChatOpenAI(model_name=model_name, temperature=LLM_TEMPERATURE)
            result = llm(messages)
            return result.content.strip()
        except Exception:
            pass

    # Fallback: preserve friendly, domain-aware greeting without hardcoding a full static message.
    base = (
        "Hello from SecureOps AI. I am here to help you with security inquiries about alerts, endpoint status, "
        "identity activity, incident handling, and threat hunting."
    )
    if "alert" in user_prompt.lower():
        return base + " You can ask me to check specific alerts, summarize alert trends, or inspect SIEM findings."
    if "workstation" in user_prompt.lower() or "endpoint" in user_prompt.lower() or "device" in user_prompt.lower():
        return base + " I can help you investigate endpoint health and malware detections for your devices."
    if "login" in user_prompt.lower() or "user" in user_prompt.lower():
        return base + " I can review login history and user activity across IAM systems."
    return base + " Ask a security-focused question and I’ll route it to the correct SOC specialist."