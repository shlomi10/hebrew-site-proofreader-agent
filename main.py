import argparse
import json
import sys
import webbrowser
from pathlib import Path

from runner import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Website spelling checker agent")
    parser.add_argument("url", nargs="?", help="Website URL")
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
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the Streamlit GUI",
    )
    args = parser.parse_args()

    if args.gui:
        import subprocess
        import sys

        ui_dir = Path(__file__).resolve().parent / "ui"
        raise SystemExit(
            subprocess.call(
                [sys.executable, "-m", "streamlit", "run", "app.py"],
                cwd=str(ui_dir),
            )
        )

    if not args.url:
        parser.error("url is required unless --gui is used")

    try:
        report = run_pipeline(
            args.url,
            max_pages=args.max_pages,
            extract_only=args.extract_only,
            model=args.model,
            skip_benchmark=args.skip_benchmark,
            on_progress=lambda u: print(u.message, file=sys.stderr),
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc

    if args.html and not args.extract_only:
        from reporting import write_html_report

        html_path = Path(args.html)
        write_html_report(str(html_path), report, args.url)
        print(f"HTML report saved to {html_path.resolve()}", file=sys.stderr)
        if args.open:
            webbrowser.open(html_path.resolve().as_uri())
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
