import sys

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from tqdm import tqdm

from analysis.schemas import TextAnalysisResult, TextIssue
from analysis.text_utils import split_text
from config import OLLAMA_BASE_URL, OLLAMA_MODEL

SYSTEM_PROMPT_HE = """אתה בודק טקסט שחולץ מאתר אינטרנט בעברית.
מצא רק בעיות אמיתיות:
1. שגיאות כתיב
2. שגיאות דקדוק
3. ניסוחים חשודים (דחיפות מוגזמת, הבטחות לא ריאליות, ניסוח פישינג)

אל תדווח על שמות מותג, קיצורים טכניים, או מילים באנגלית שנפוצות באתרים ישראליים.
אם אין בעיות, החזר רשימת errors ריקה."""

SYSTEM_PROMPT_EN = """You are proofreading text extracted from an English website.
Find only real issues:
1. Spelling errors
2. Grammar errors
3. Suspicious phrasing (excessive urgency, unrealistic promises, phishing-style wording)

Do not flag brand names, technical abbreviations, or intentional stylistic choices.
If there are no issues, return an empty errors list."""


def _build_agent(model: str, language: str):
    system_prompt = SYSTEM_PROMPT_HE if language == "he" else SYSTEM_PROMPT_EN
    llm = ChatOllama(
        model=model,
        base_url=OLLAMA_BASE_URL,
        temperature=0,
    )
    return create_agent(
        llm,
        system_prompt=system_prompt,
        response_format=TextAnalysisResult,
    )


def _merge_results(results: list[TextAnalysisResult]) -> TextAnalysisResult:
    seen: set[tuple[str, str, str]] = set()
    merged: list[TextIssue] = []
    for result in results:
        for issue in result.errors:
            key = (issue.type, issue.original, issue.suggestion)
            if key in seen:
                continue
            seen.add(key)
            merged.append(issue)
    return TextAnalysisResult(errors=merged)


def analyze_text(
    text: str,
    model: str | None = None,
    language: str = "he",
) -> TextAnalysisResult:
    chunks = split_text(text)
    if not chunks:
        return TextAnalysisResult()

    selected_model = model or OLLAMA_MODEL
    agent = _build_agent(selected_model, language)
    chunk_results: list[TextAnalysisResult] = []

    prompt_he = "בדוק את קטע הטקסט {index}/{total}:\n\n{chunk}"
    prompt_en = "Proofread text chunk {index}/{total}:\n\n{chunk}"

    for index, chunk in enumerate(
        tqdm(chunks, desc="Analyzing chunks", unit="chunk", file=sys.stderr),
        start=1,
    ):
        content = (
            prompt_he.format(index=index, total=len(chunks), chunk=chunk)
            if language == "he"
            else prompt_en.format(index=index, total=len(chunks), chunk=chunk)
        )
        response = agent.invoke({"messages": [HumanMessage(content=content)]})
        structured = response.get("structured_response")
        if isinstance(structured, TextAnalysisResult):
            chunk_results.append(structured)
        elif isinstance(structured, dict):
            chunk_results.append(TextAnalysisResult.model_validate(structured))

    return _merge_results(chunk_results)
