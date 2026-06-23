import argparse
import json
import sys
import webbrowser
from pathlib import Path

from crawl import crawl_site, extract_visible_text


def main() -> None:
    parser = argparse.ArgumentParser(description="Website spelling checker agent")
    parser.add_argument("url", help="Website URL")
    parser.add_argument("--max-pages", type=int, default=1)
    parser.add_argument("--extract-only", action="store_true")
    parser.add_argument(
        "--html",
        nargs="?",
        const="report.html",
        metavar="FILE",
        help="Write HTML report (default: report.html)",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open HTML report in browser",
    )
    parser.add_argument(
        "--model",
        metavar="NAME",
        help="Skip auto-selection and use this Ollama model",
    )
    parser.add_argument(
        "--skip-benchmark",
        action="store_true",
        help="Skip model benchmark (use config default or --model)",
    )
    args = parser.parse_args()

    if args.max_pages == 1:
        print(f"Opening {args.url} with Playwright...", file=sys.stderr)
        text = extract_visible_text(args.url)
        pages = {args.url: text}
    else:
        print(f"Crawling {args.url} (max {args.max_pages} pages)...", file=sys.stderr)
        pages = crawl_site(args.url, max_pages=args.max_pages)

    if args.extract_only:
        output = {
            url: {"char_count": len(text), "text": text}
            for url, text in pages.items()
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    from analysis import (
        SUPPORTED_LANGUAGES,
        analyze_text,
        detect_language,
        ensure_ollama_ready,
        format_selection_report,
        select_best_model,
    )
    from config import OLLAMA_MODEL
    from reporting import write_html_report

    combined_text = "\n".join(
        text for text in pages.values() if not text.startswith("[ERROR]")
    )
    lang_result = detect_language(combined_text)

    if lang_result.language not in SUPPORTED_LANGUAGES:
        if lang_result.language == "unknown":
            print(
                "Could not detect language. Supported: Hebrew (he), English (en).",
                file=sys.stderr,
            )
        else:
            print(
                f"Unsupported language: {lang_result.name} ({lang_result.language}).\n"
                "This agent supports Hebrew and English only.",
                file=sys.stderr,
            )
        raise SystemExit(1)

    print(
        f"Detected language: {lang_result.name} "
        f"(confidence: {lang_result.confidence:.0%})",
        file=sys.stderr,
    )

    if args.model:
        selected_model = args.model
        model_selection = None
        ensure_ollama_ready(selected_model)
        print(f"Using model from CLI: {selected_model}", file=sys.stderr)
    elif args.skip_benchmark:
        selected_model = OLLAMA_MODEL
        model_selection = None
        ensure_ollama_ready(selected_model)
        print(f"Using config model: {selected_model}", file=sys.stderr)
    else:
        installed = ensure_ollama_ready()
        print("Running model benchmark (6+ candidates)...", file=sys.stderr)
        model_selection = select_best_model(
            combined_text, lang_result.language, installed
        )
        selected_model = model_selection.model
        print(format_selection_report(model_selection, lang_result.language), file=sys.stderr)

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

    for url, text in pages.items():
        print(f"Analyzing {url} ({len(text)} chars)...", file=sys.stderr)
        if text.startswith("[ERROR]"):
            report[url] = {"error": text, "issues": []}
            continue
        analysis = analyze_text(text, model=selected_model, language=lang_result.language)
        report[url] = {
            "char_count": len(text),
            "issue_count": len(analysis.errors),
            "issues": [issue.model_dump() for issue in analysis.errors],
        }

    if args.html:
        html_path = Path(args.html)
        write_html_report(str(html_path), report, args.url)
        print(f"HTML report saved to {html_path.resolve()}", file=sys.stderr)
        if args.open:
            webbrowser.open(html_path.resolve().as_uri())
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
