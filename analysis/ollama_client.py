import sys

import httpx

from config import OLLAMA_BASE_URL, OLLAMA_MODEL


def get_installed_models() -> set[str]:
    try:
        response = httpx.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3.0)
        response.raise_for_status()
    except httpx.HTTPError:
        return set()
    models = response.json().get("models", [])
    return {model.get("name", "") for model in models if model.get("name")}


def ensure_ollama_ready(model: str | None = None) -> set[str]:
    target = model or OLLAMA_MODEL
    try:
        response = httpx.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3.0)
        response.raise_for_status()
    except httpx.HTTPError:
        print(
            "Ollama is not running.\n"
            "1. Install from https://ollama.com/download/windows\n"
            "2. Open a new terminal after install\n"
            "3. Run: ollama pull <model>\n"
            "4. Retry this command",
            file=sys.stderr,
        )
        raise SystemExit(1)

    installed = get_installed_models()
    model_base = target.split(":")[0]
    if target not in installed and not any(
        name.startswith(model_base) for name in installed
    ):
        print(
            f"Model '{target}' is not installed.\n"
            f"Run: ollama pull {target}",
            file=sys.stderr,
        )
        raise SystemExit(1)
    return installed
