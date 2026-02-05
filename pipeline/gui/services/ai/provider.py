# services/ai/provider.py
import os
import logging
from .ollama_provider import call_ollama
from .groq_provider import call_groq

AI_MODE = os.getenv("AI_MODE", "hybrid").lower()  # "ollama", "groq", or "hybrid"


def run_ai_task(task: str, payload: dict) -> dict:
    """
    Canonical AI entry point.
    The API layer builds the payload using prompt_builder.
    This function routes to the active provider with fallback logic.
    """

    logging.info(f"[AI] Running task '{task}' via mode '{AI_MODE}'")

    # -----------------------------
    # MODE: GROQ ONLY
    # -----------------------------
    if AI_MODE == "groq":
        logging.info("[AI] Using Groq provider (forced mode)")
        return call_groq(task, payload)

    # -----------------------------
    # MODE: OLLAMA ONLY
    # -----------------------------
    if AI_MODE == "ollama":
        logging.info("[AI] Using Ollama provider (forced mode)")
        return call_ollama(task, payload)

    # -----------------------------
    # MODE: HYBRID (Ollama → Groq)
    # -----------------------------
    if AI_MODE == "hybrid":
        logging.info("[AI] Using hybrid mode (Ollama → Groq fallback)")

        # 1. Try Ollama first
        try:
            logging.info("[AI] Trying Ollama first...")
            result = call_ollama(task, payload)

            if isinstance(result, dict) and result.get("status") != "error":
                logging.info("[AI] Ollama succeeded")
                return result

            logging.warning("[AI] Ollama returned an error, falling back to Groq")

        except Exception as e:
            logging.error(f"[AI] Ollama exception: {e}")
            logging.warning("[AI] Falling back to Groq")

        # 2. Try Groq second
        try:
            logging.info("[AI] Trying Groq fallback...")
            return call_groq(task, payload)

        except Exception as e:
            logging.error(f"[AI] Groq exception: {e}")
            return {"status": "error", "message": "Both Ollama and Groq failed"}

    # -----------------------------
    # Unknown mode
    # -----------------------------
    logging.error(f"[AI] Unknown AI_MODE '{AI_MODE}'")
    return {"status": "error", "message": f"Unknown AI_MODE '{AI_MODE}'"}
