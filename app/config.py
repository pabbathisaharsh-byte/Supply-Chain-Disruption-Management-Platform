# app/config.py
"""
Purpose: App Configuration (All Members)
Role:
- Loads system environment variables.
- Houses mock data properties or API configurations.
"""

import os

# Base API Configuration (Mocked REST API endpoints for the capstone)
SIEM_API_ENDPOINT = os.getenv("SIEM_API_ENDPOINT", "https://api.mocksiem.local/v1")
EDR_API_ENDPOINT = os.getenv("EDR_API_ENDPOINT", "https://api.mockedr.local/v1")
IAM_API_ENDPOINT = os.getenv("IAM_API_ENDPOINT", "https://api.mockiam.local/v1")

# LLM Config
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.0"))
