from collections.abc import Callable
from dataclasses import dataclass

from crawl import crawl_site, extract_visible_text


@dataclass(frozen=True)
class ProgressUpdate:
    stage: str
    message: str
    percent: float | None = None


def _emit(
    callback: Callable[[ProgressUpdate], None] | None,
    stage: str,
    message: str,
    percent: float | None = None,
) -> None:
    if callback:
        callback(ProgressUpdate(stage=stage, message=message, percent=percent))


def run_pipeline(
    url: str,
    max_pages: int = 1,
    extract_only: bool = False,
    model: str | None = None,
    skip_benchmark: bool = False,
    on_progress: Callable[[ProgressUpdate], None] | None = None,
) -> dict[str, object]:
    if max_pages == 1:
        _emit(on_progress, "extract", f"Opening {url} with Playwright...", 0.1)
        text = extract_visible_text(url)
        pages = {url: text}
    else:
        _emit(on_progress, "crawl", f"Crawling {url} (max {max_pages} pages)...", 0.1)
        pages = crawl_site(url, max_pages=max_pages)

    if extract_only:
        return {
            url: {"char_count": len(text), "text": text}
            for url, text in pages.items()
        }

    from analysis import (
        SUPPORTED_LANGUAGES,
        analyze_text,
        detect_language,
        ensure_ollama_ready,
        select_best_model,
    )
    from config import OLLAMA_MODEL

    combined_text = "\n".join(
        text for text in pages.values() if not text.startswith("[ERROR]")
    )
    _emit(on_progress, "language", "Detecting language...", 0.2)
    lang_result = detect_language(combined_text)

    if lang_result.language not in SUPPORTED_LANGUAGES:
        if lang_result.language == "unknown":
            raise ValueError(
                "Could not detect language. Supported: Hebrew (he), English (en)."
            )
        raise ValueError(
            f"Unsupported language: {lang_result.name} ({lang_result.language}). "
            "This agent supports Hebrew and English only."
        )

    model_selection = None
    if model:
        selected_model = model
        _emit(on_progress, "ollama", f"Using model: {selected_model}", 0.35)
        ensure_ollama_ready(selected_model)
    elif skip_benchmark:
        selected_model = OLLAMA_MODEL
        _emit(on_progress, "ollama", f"Using config model: {selected_model}", 0.35)
        ensure_ollama_ready(selected_model)
    else:
        _emit(on_progress, "benchmark", "Benchmarking models (6+ candidates)...", 0.3)
        installed = ensure_ollama_ready()
        model_selection = select_best_model(
            combined_text, lang_result.language, installed
        )
        selected_model = model_selection.model
        _emit(on_progress, "benchmark", f"Selected model: {selected_model}", 0.45)

    report: dict[str, object] = {
        "language": {
            "code": lang_result.language,
            "name": lang_result.name,
            "confidence": round(lang_result.confidence, 3),
        },
        "model": selected_model,
    }
    if model_selection:
        report["model_selection"] = model_selection.model_dump()

    page_count = len(pages)
    for index, (page_url, text) in enumerate(pages.items(), start=1):
        base = 0.5 + (index - 1) / page_count * 0.45
        _emit(
            on_progress,
            "analyze",
            f"Analyzing {page_url} ({len(text)} chars)...",
            base,
        )
        if text.startswith("[ERROR]"):
            report[page_url] = {"error": text, "issues": []}
            continue
        analysis = analyze_text(
            text, model=selected_model, language=lang_result.language
        )
        report[page_url] = {
            "char_count": len(text),
            "issue_count": len(analysis.errors),
            "issues": [issue.model_dump() for issue in analysis.errors],
        }

    _emit(on_progress, "done", "Analysis complete.", 1.0)
    return report
