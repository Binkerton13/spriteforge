# services/ai/ollama_provider.py
import json
import logging
import requests
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")


def call_ollama(task: str, payload: dict) -> dict:
    """
    Sends a strict JSON payload to a local Ollama model.
    """
    try:
        r = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3:latest",
                "prompt": json.dumps(payload),
                "stream": False
            },
            timeout=60
        )
        r.raise_for_status()

        data = r.json()
        raw = data.get("response", "")

        # Extract the first JSON object from the response
        start = raw.find("{")
        end = raw.rfind("}") + 1

        if start != -1 and end != -1:
            json_str = raw[start:end]
            try:
                print("Ollama extracted JSON string:", json_str)
                return json.loads(json_str)
            except Exception as e:
                logging.error(f"[AI][Ollama] JSON parse error: {e}")
                logging.error(f"[AI][Ollama] Extracted JSON: {json_str}")
                return {"status": "error", "message": "Invalid JSON from Ollama"}

        # If no JSON found at all
        logging.error(f"[AI][Ollama] No JSON found in response: {raw}")
        return {"status": "error", "message": "No JSON found in Ollama response"}

    except Exception as e:
        logging.error(f"[AI][Ollama] Error: {e}")
        return {"status": "error", "message": str(e)}
