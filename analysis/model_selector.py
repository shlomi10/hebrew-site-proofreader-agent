import json
import sys
import time
from dataclasses import dataclass

import httpx
from tqdm import tqdm

from analysis.schemas import ModelBenchmarkResult, ModelSelection
from config import OLLAMA_BASE_URL

BENCHMARK_SAMPLE_SIZE = 400

BENCHMARK_PROMPT_HE = """בדוק את קטע הטקסט הבא לשגיאות כתיב, דקדוק וניסוח חשוד.
החזר JSON בלבד בפורמט: {{"errors": [{{"type": "spelling|grammar|suspicious_phrasing", "original": "...", "suggestion": "...", "reason": "..."}}]}}

טקסט:
{sample}"""

BENCHMARK_PROMPT_EN = """Proofread the following text for spelling, grammar, and suspicious phrasing.
Return JSON only in this format: {{"errors": [{{"type": "spelling|grammar|suspicious_phrasing", "original": "...", "suggestion": "...", "reason": "..."}}]}}

Text:
{sample}"""


@dataclass(frozen=True)
class ModelCandidate:
    name: str
    match_prefixes: tuple[str, ...]
    hebrew_prior: float
    english_prior: float
    description: str
    rationale_he: str
    rationale_en: str


HEBREW_CANDIDATES: tuple[ModelCandidate, ...] = (
    ModelCandidate(
        "aminadaven/dictalm2.0-instruct:q4_k_m",
        ("aminadaven/dictalm", "dictalm"),
        30.0,
        5.0,
        "DictaLM 2.0 Instruct — Hebrew-specialized LM by Dicta",
        "DictaLM 2.0 אומן במיוחד על קורפוס עברי (כתיב, דקדוק, ניסוח) ומנצח במודלים כלליים בבדיקת אתרים בעברית.",
        "DictaLM is Hebrew-specialized; not optimal for English sites.",
    ),
    ModelCandidate(
        "llama3.2",
        ("llama3.2",),
        18.0,
        28.0,
        "Meta Llama 3.2 — strong multilingual general model",
        "Llama 3.2 תומך בעברית אך לא מותאם ספציפית אליה; מתאים כגיבוי כש-DictaLM לא מותקן.",
        "Llama 3.2 excels at English grammar and spelling with broad training data.",
    ),
    ModelCandidate(
        "mistral",
        ("mistral",),
        16.0,
        26.0,
        "Mistral — efficient European multilingual model",
        "Mistral מציג ביצועים סבירים בעברית אך פחות מדויק ממודלים עבריים ייעודיים.",
        "Mistral is fast and accurate for English proofreading tasks.",
    ),
    ModelCandidate(
        "qwen2.5",
        ("qwen2.5",),
        17.0,
        27.0,
        "Qwen 2.5 — Alibaba multilingual model with strong reasoning",
        "Qwen 2.5 מטפל היטב בשפות רבות כולל עברית, אך ללא התמחות עברית עמוקה.",
        "Qwen 2.5 scores highly on English benchmarks and structured output.",
    ),
    ModelCandidate(
        "gemma2",
        ("gemma2",),
        15.0,
        25.0,
        "Google Gemma 2 — compact general-purpose model",
        "Gemma 2 קומפקטי ומהיר; מתאים לעברית בסיסית אך לא לדיוק מקסימלי.",
        "Gemma 2 offers solid English quality with low resource usage.",
    ),
    ModelCandidate(
        "phi3",
        ("phi3",),
        12.0,
        22.0,
        "Microsoft Phi-3 — small but capable instruction model",
        "Phi-3 קטן ומהיר; מוגבל בדיוק עברי לעומת מודלים גדולים יותר.",
        "Phi-3 is efficient for English on modest hardware.",
    ),
    ModelCandidate(
        "aya",
        ("aya",),
        14.0,
        20.0,
        "Cohere Aya — explicitly multilingual (23+ languages)",
        "Aya תוכנן לרב-לשוניות כולל עברית, אך בדרך כלל פחות מדויק מ-DictaLM.",
        "Aya handles many languages but English-specific models often outperform it.",
    ),
)

ENGLISH_CANDIDATES: tuple[ModelCandidate, ...] = (
    ModelCandidate(
        "llama3.2",
        ("llama3.2",),
        18.0,
        28.0,
        "Meta Llama 3.2 — strong English instruction following",
        "Llama 3.2 is general-purpose; English sites are better served by this than Hebrew-only models.",
        "Llama 3.2 leads on English spelling/grammar with reliable structured JSON output.",
    ),
    ModelCandidate(
        "llama3.1",
        ("llama3.1",),
        17.0,
        27.0,
        "Meta Llama 3.1 — predecessor with excellent English",
        "Llama 3.1 is strong in English; preferred over Hebrew-specialized models for English sites.",
        "Llama 3.1 remains a top English proofreading choice with large context.",
    ),
    ModelCandidate(
        "mistral",
        ("mistral",),
        16.0,
        26.0,
        "Mistral — fast European model, strong English",
        "Mistral works for English; Hebrew-specific models would underperform here.",
        "Mistral balances speed and English accuracy very well.",
    ),
    ModelCandidate(
        "qwen2.5",
        ("qwen2.5",),
        17.0,
        27.0,
        "Qwen 2.5 — high benchmark scores on English tasks",
        "Qwen 2.5 handles English excellently; better fit than DictaLM for English content.",
        "Qwen 2.5 ranks among the best open models for English reasoning and grammar.",
    ),
    ModelCandidate(
        "gemma2",
        ("gemma2",),
        15.0,
        25.0,
        "Google Gemma 2 — efficient English model",
        "Gemma 2 is adequate for English; specialized English models score higher.",
        "Gemma 2 delivers good English quality with lower VRAM requirements.",
    ),
    ModelCandidate(
        "phi3",
        ("phi3",),
        12.0,
        22.0,
        "Microsoft Phi-3 — lightweight English-capable model",
        "Phi-3 is a fallback for English when larger models are unavailable.",
        "Phi-3 is a practical English option on limited hardware.",
    ),
    ModelCandidate(
        "deepseek-r1",
        ("deepseek-r1", "deepseek-r1:"),
        13.0,
        24.0,
        "DeepSeek R1 — reasoning-focused model",
        "DeepSeek R1 can analyze English but is slower; better English alternatives exist.",
        "DeepSeek R1 offers deep reasoning for complex English phrasing issues.",
    ),
)


def _candidates_for_language(language: str) -> tuple[ModelCandidate, ...]:
    if language == "he":
        return HEBREW_CANDIDATES
    return ENGLISH_CANDIDATES


def _resolve_installed(candidate: ModelCandidate, installed: set[str]) -> str | None:
    for installed_name in sorted(installed):
        lowered = installed_name.lower()
        for prefix in candidate.match_prefixes:
            if lowered.startswith(prefix.lower()) or prefix.lower() in lowered:
                return installed_name
    return None


def _benchmark_model(
    model: str,
    sample: str,
    language: str,
) -> tuple[float, float, bool, str]:
    prompt_template = BENCHMARK_PROMPT_HE if language == "he" else BENCHMARK_PROMPT_EN
    prompt = prompt_template.format(sample=sample[:BENCHMARK_SAMPLE_SIZE])

    start = time.perf_counter()
    try:
        response = httpx.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "format": "json",
            },
            timeout=180.0,
        )
        response.raise_for_status()
        elapsed = time.perf_counter() - start
        body = response.json()
        raw = body.get("response", "")
        parsed = json.loads(raw)
        errors = parsed.get("errors", [])
        if not isinstance(errors, list):
            return 0.0, elapsed, False, "invalid errors field"
        if len(errors) > 50:
            return 5.0, elapsed, True, "too many issues (possible hallucination)"
        return 20.0, elapsed, True, ""
    except (httpx.HTTPError, json.JSONDecodeError, KeyError, TypeError) as exc:
        elapsed = time.perf_counter() - start
        return 0.0, elapsed, False, str(exc)


def _latency_score(elapsed: float) -> float:
    if elapsed <= 5:
        return 15.0
    if elapsed <= 15:
        return 15.0 - (elapsed - 5) * 0.8
    if elapsed <= 45:
        return 7.0 - (elapsed - 15) * 0.15
    return 0.0


def select_best_model(
    text: str,
    language: str,
    installed_models: set[str],
) -> ModelSelection:
    candidates = _candidates_for_language(language)
    sample = text.strip()[:BENCHMARK_SAMPLE_SIZE]
    if not sample:
        sample = "בדיקת טקסט לדוגמה." if language == "he" else "Sample text for benchmarking."

    benchmarks: list[ModelBenchmarkResult] = []
    resolved: list[tuple[ModelCandidate, str]] = []

    for candidate in candidates:
        installed_name = _resolve_installed(candidate, installed_models)
        if installed_name:
            resolved.append((candidate, installed_name))

    if not resolved:
        fallback = sorted(installed_models)[0] if installed_models else ""
        return ModelSelection(
            model=fallback,
            language=language,
            rationale="No catalog candidates installed; using first available model.",
            benchmarks=[],
            candidates_compared=0,
        )

    for candidate, installed_name in tqdm(
        resolved,
        desc="Benchmarking models",
        unit="model",
        file=sys.stderr,
    ):
        prior = candidate.hebrew_prior if language == "he" else candidate.english_prior
        json_score, elapsed, valid_json, error = _benchmark_model(
            installed_name, sample, language
        )
        latency_score = _latency_score(elapsed) if valid_json else 0.0
        total = prior + json_score + latency_score
        benchmarks.append(
            ModelBenchmarkResult(
                model=installed_name,
                catalog_name=candidate.name,
                description=candidate.description,
                prior_score=prior,
                json_score=json_score,
                latency_seconds=round(elapsed, 2),
                latency_score=round(latency_score, 2),
                total_score=round(total, 2),
                installed=True,
                valid_json=valid_json,
                error=error,
            )
        )

    for candidate in candidates:
        if _resolve_installed(candidate, installed_models):
            continue
        prior = candidate.hebrew_prior if language == "he" else candidate.english_prior
        benchmarks.append(
            ModelBenchmarkResult(
                model=candidate.name,
                catalog_name=candidate.name,
                description=candidate.description,
                prior_score=prior,
                json_score=0.0,
                latency_seconds=0.0,
                latency_score=0.0,
                total_score=round(prior * 0.3, 2),
                installed=False,
                valid_json=False,
                error="not installed",
            )
        )

    installed_benchmarks = [b for b in benchmarks if b.installed and b.valid_json]
    if installed_benchmarks:
        winner_entry = max(installed_benchmarks, key=lambda b: b.total_score)
    else:
        installed_any = [b for b in benchmarks if b.installed]
        winner_entry = max(installed_any, key=lambda b: b.total_score) if installed_any else benchmarks[0]

    winner_candidate = next(
        (c for c, name in resolved if name == winner_entry.model),
        candidates[0],
    )
    rationale = (
        winner_candidate.rationale_he
        if language == "he"
        else winner_candidate.rationale_en
    )
    rationale += (
        f" Benchmark score: {winner_entry.total_score}/65 "
        f"(prior={winner_entry.prior_score}, json={winner_entry.json_score}, "
        f"latency={winner_entry.latency_score}, {winner_entry.latency_seconds}s)."
    )

    compared = len(resolved)
    return ModelSelection(
        model=winner_entry.model,
        language=language,
        rationale=rationale,
        benchmarks=sorted(benchmarks, key=lambda b: b.total_score, reverse=True),
        candidates_compared=compared,
    )


def format_selection_report(selection: ModelSelection, language: str) -> str:
    lines: list[str] = []
    if language == "he":
        lines.append(f"שפה שזוהתה: עברית")
        lines.append(f"מודל נבחר: {selection.model}")
        lines.append(f"הסבר: {selection.rationale}")
        lines.append("")
        lines.append(f"השוואה מדעית ({len(selection.benchmarks)} מודלים בקטלוג, {selection.candidates_compared} מותקנים ונבדקו):")
        lines.append(f"{'מודל':<40} {'מותקן':<8} {'JSON':<6} {'זמן':<8} {'ציון':<8}")
        for b in selection.benchmarks:
            lines.append(
                f"{b.model:<40} {'כן' if b.installed else 'לא':<8} "
                f"{'כן' if b.valid_json else 'לא':<6} "
                f"{b.latency_seconds:<8} {b.total_score:<8}"
            )
    else:
        lines.append(f"Detected language: English")
        lines.append(f"Selected model: {selection.model}")
        lines.append(f"Rationale: {selection.rationale}")
        lines.append("")
        lines.append(
            f"Scientific comparison ({len(selection.benchmarks)} catalog models, "
            f"{selection.candidates_compared} installed and benchmarked):"
        )
        lines.append(f"{'Model':<40} {'Inst':<6} {'JSON':<6} {'Time':<8} {'Score':<8}")
        for b in selection.benchmarks:
            lines.append(
                f"{b.model:<40} {'yes' if b.installed else 'no':<6} "
                f"{'yes' if b.valid_json else 'no':<6} "
                f"{b.latency_seconds:<8} {b.total_score:<8}"
            )
    return "\n".join(lines)
