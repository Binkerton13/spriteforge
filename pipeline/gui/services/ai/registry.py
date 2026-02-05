# services/ai/registry.py

from services.ai.groq_provider import call_groq
from services.ai.ollama_provider import call_ollama

PROVIDERS = {
    "groq": call_groq,
    "ollama": call_ollama,
    # "openai": call_openai,        # future
    # "anthropic": call_anthropic,  # future
}
