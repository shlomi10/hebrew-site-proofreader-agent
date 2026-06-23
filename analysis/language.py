import re
from dataclasses import dataclass

from langdetect import DetectorFactory, detect_langs

DetectorFactory.seed = 0

HEBREW_RE = re.compile(r"[\u0590-\u05FF]")
LATIN_RE = re.compile(r"[A-Za-z]")

SUPPORTED_LANGUAGES = {
    "he": "Hebrew",
    "en": "English",
}


@dataclass(frozen=True)
class LanguageDetection:
    language: str
    name: str
    confidence: float
    hebrew_ratio: float
    latin_ratio: float


def _script_ratios(text: str) -> tuple[float, float]:
    hebrew = len(HEBREW_RE.findall(text))
    latin = len(LATIN_RE.findall(text))
    total = hebrew + latin
    if total == 0:
        return 0.0, 0.0
    return hebrew / total, latin / total


def detect_language(text: str) -> LanguageDetection:
    sample = text.strip()
    if not sample:
        return LanguageDetection("unknown", "Unknown", 0.0, 0.0, 0.0)

    hebrew_ratio, latin_ratio = _script_ratios(sample)

    if hebrew_ratio >= 0.55:
        return LanguageDetection("he", "Hebrew", hebrew_ratio, hebrew_ratio, latin_ratio)
    if latin_ratio >= 0.55:
        return LanguageDetection("en", "English", latin_ratio, hebrew_ratio, latin_ratio)

    try:
        candidates = detect_langs(sample[:5000])
    except Exception:
        if hebrew_ratio > latin_ratio:
            return LanguageDetection("he", "Hebrew", hebrew_ratio, hebrew_ratio, latin_ratio)
        if latin_ratio > hebrew_ratio:
            return LanguageDetection("en", "English", latin_ratio, hebrew_ratio, latin_ratio)
        return LanguageDetection("unknown", "Unknown", 0.0, hebrew_ratio, latin_ratio)

    if not candidates:
        return LanguageDetection("unknown", "Unknown", 0.0, hebrew_ratio, latin_ratio)

    best = candidates[0]
    lang = best.lang
    if lang in SUPPORTED_LANGUAGES:
        return LanguageDetection(
            lang,
            SUPPORTED_LANGUAGES[lang],
            best.prob,
            hebrew_ratio,
            latin_ratio,
        )

    return LanguageDetection(lang, lang, best.prob, hebrew_ratio, latin_ratio)
