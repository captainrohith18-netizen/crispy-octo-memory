from __future__ import annotations

import requests


def detect_ollama_models() -> list[str]:
    """Return all locally available Ollama model names from the Ollama API."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code != 200:
            return []
        payload = response.json()
    except Exception:
        return []

    models = payload.get("models", [])
    names: list[str] = []
    for model in models:
        name = model.get("name") or model.get("model") or ""
        if name:
            names.append(name)
    return names


def resolve_ollama_model() -> dict:
    """Choose the best model according to the workshop policy: Qwen > Llama > not available."""
    available = detect_ollama_models()
    if not available:
        return {
            "model": None,
            "available_models": [],
            "reason": "Ollama is not running or no Qwen/Llama model is installed.",
            "message": "No local Ollama model was detected. Install Qwen or Llama with 'ollama pull qwen3' or 'ollama pull llama3.2'.",
        }

    lowered = [name.lower() for name in available]
    qwen_models = [name for name in available if "qwen" in name.lower()]
    if qwen_models:
        return {"model": qwen_models[0], "available_models": available, "reason": "Qwen detected", "message": "Qwen selected as the primary local model."}

    llama_models = [name for name in available if "llama" in name.lower()]
    if llama_models:
        return {"model": llama_models[0], "available_models": available, "reason": "Llama detected", "message": "Qwen was not found, so a locally installed Llama model was selected."}

    return {
        "model": None,
        "available_models": available,
        "reason": "No compatible model family found",
        "message": "A compatible Qwen or Llama model was not detected. Install one before running the app.",
    }
