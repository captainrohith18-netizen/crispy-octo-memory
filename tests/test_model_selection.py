from unittest.mock import patch

from core.model_selector import resolve_ollama_model


def test_qwen_is_preferred_when_available():
    with patch("core.model_selector.detect_ollama_models", return_value=["llama3.2", "qwen3"]):
        result = resolve_ollama_model()
        assert result["model"] == "qwen3"


def test_no_compatible_model_returns_clear_message():
    with patch("core.model_selector.detect_ollama_models", return_value=["mistral", "phi3"]):
        result = resolve_ollama_model()
        assert result["model"] is None
        assert "Install" in result["message"] or "compatible" in result["message"]
