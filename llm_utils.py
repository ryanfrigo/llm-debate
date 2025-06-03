"""
Utility functions for interacting with the OpenRouter API via the openai library.
"""
import openai
from typing import List, Dict, Optional
import sys

from config import OPENROUTER_API_KEY, HTTP_REFERER, X_TITLE

def initialize_client(api_key: Optional[str] = None, base_url: str = "https://openrouter.ai/api/v1"):
    """
    Initializes and returns an OpenAI client for OpenRouter.
    """
    api_key = api_key or OPENROUTER_API_KEY
    try:
        client = openai.OpenAI(api_key=api_key, base_url=base_url)
        return client
    except Exception as e:
        print(f"[Error] Failed to initialize OpenAI client: {e}", file=sys.stderr)
        sys.exit(1)

def get_llm_response(
    client,
    model: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
) -> str:
    """
    Calls the LLM and returns the response text. Handles API errors gracefully.
    """
    headers = {}
    if HTTP_REFERER:
        headers["HTTP-Referer"] = HTTP_REFERER
    if X_TITLE:
        headers["X-Title"] = X_TITLE
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            extra_headers=headers if headers else None,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[Error] LLM API call failed: {e}", file=sys.stderr)
        return "[Error: LLM API call failed]" 