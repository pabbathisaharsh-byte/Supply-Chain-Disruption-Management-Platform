# app/main.py
"""
Purpose: App Entry Point (All Members)
Role:
- Main initializer for SecureOps AI.
- Boots UI elements, loads API settings, and coordinates conversation flows.
"""

import sys
from app.config import LLM_MODEL
from app.ui.chat import render_chat_interface

def main():
    print(f"Initializing SecureOps AI SOC Assistant using model {LLM_MODEL}...")
    print("Connecting to Mock REST APIs for SIEM, EDR, IAM, and Threat Intel...")
    # Executing the chat front-end
    render_chat_interface()

if __name__ == "__main__":
    main()