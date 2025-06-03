# config.py
"""
Configuration constants for the LLM Debate Workflow.
Uses environment variables for sensitive values.
"""

import os

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "YOUR_OPENROUTER_API_KEY")
HTTP_REFERER = os.environ.get("HTTP_REFERER", "")  # Optional: e.g., 'https://your-site.com'
X_TITLE = os.environ.get("X_TITLE", "")             # Optional: e.g., 'Your App Name'

PERSPECTIVE_GENERATION_MODEL = "deepseek/deepseek-chat-v3-0324:free"
DEBATE_AGENT_MODEL = "deepseek/deepseek-chat-v3-0324:free"
NUM_PERSPECTIVES_TO_GENERATE = 3
NUM_DEBATE_ROUNDS = 3
