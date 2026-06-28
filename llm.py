"""
Description: Local Ollama Inference Wrapper. Wraps the Ollama runtime and uses deterministic decoding parameterizations with JSON serialization mode constraint.
Author: Sudeep Varma K
Date: 2026-06-27
"""
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"


def ask(prompt, system_prompt="", force_json=False):
    """Executes target system instructions against local Ollama container endpoints."""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "system": system_prompt,
        "stream": False,
        "options": {
            "temperature": 0.0
        }
    }

    if force_json:
        payload["format"] = "json"

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "")
        return f"Error: HTTP {response.status_code}"
    except Exception as e:
        return f"Ollama Connection Error: {str(e)}"