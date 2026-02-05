# services/ai/groq_provider.py
import json
import logging
import requests
import os

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
def get_groq_key():
    return os.getenv("GROQ_API_KEY")
GROQ_KEY = get_groq_key()

def call_groq(task: str, payload: dict) -> dict:
    """
    Sends a strict JSON payload to Groq.
    """
    print("GROQ_KEY:", GROQ_KEY)
    try:
        r = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "Return only strict JSON."},
                    {"role": "user", "content": json.dumps(payload)}
                ],
                "temperature": 0.2
            },
            timeout=60
        )
        r.raise_for_status()

        content = r.json()["choices"][0]["message"]["content"]
        print("Groq response content:", content)
        return json.loads(content)

    except Exception as e:
        logging.error(f"[AI][Groq] Error: {e}")
        return {"status": "error", "message": str(e)}
