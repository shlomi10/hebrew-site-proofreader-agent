import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from config import MAX_PAGES, OLLAMA_MODEL
from reporting import write_html_report
from runner import ProgressUpdate, run_pipeline
from styles import CUSTOM_CSS, HEADER_HTML, ISSUE_TYPE_LABELS, METADATA_KEYS

FOOTER_HTML = """
<div id="cyber-footer">100% local — offline node</div>
<script>
(function () {
    function killScroll() {
        var root = document.documentElement;
        var body = document.body;
        if (!body) return;
        root.style.overflow = "hidden";
        root.style.height = "100%";
        root.style.maxHeight = "100%";
        body.style.overflow = "hidden";
        body.style.position = "fixed";
        body.style.inset = "0";
        body.style.width = "100%";
        body.style.height = "100%";
        body.style.maxHeight = "100%";
        var nodes = document.querySelectorAll(".stApp, [data-testid='stAppViewContainer'], [data-testid='stMain'], section.main, .block-container, [data-testid='stVerticalBlock'], [data-testid='stHtml']");
        for (var i = 0; i < nodes.length; i++) {
            nodes[i].style.overflow = "hidden";
            nodes[i].style.maxHeight = "100vh";
            nodes[i].style.scrollbarWidth = "none";
        }
        var style = document.getElementById("cyber-no-scroll");
        if (!style) {
            style = document.createElement("style");
            style.id = "cyber-no-scroll";
            style.textContent = "html,body,.stApp,[data-testid='stAppViewContainer'],[data-testid='stMain'],section.main,.block-container,[data-testid='stVerticalBlock']{overflow:hidden!important;max-height:100vh!important}body{position:fixed!important;inset:0!important;width:100%!important}*::-webkit-scrollbar{display:none!important;width:0!important;height:0!important}";
            document.head.appendChild(style);
        }
    }
    var el = document.getElementById("cyber-footer");
    if (el) {
        el.style.position = "fixed";
        el.style.bottom = "0.5rem";
        el.style.left = "0";
        el.style.width = "100%";
        el.style.display = "flex";
        el.style.justifyContent = "center";
        el.style.alignItems = "center";
        el.style.zIndex = "999999";
        el.style.pointerEvents = "none";
        el.style.color = "#5a7a8a";
        el.style.fontSize = "0.78rem";
        el.style.letterSpacing = "0.08em";
        el.style.textTransform = "uppercase";
        el.style.fontFamily = "'JetBrains Mono', monospace";
        el.style.direction = "ltr";
        if (el.parentElement !== document.body) {
            document.body.appendChild(el);
        }
    }
    killScroll();
    window.addEventListener("load", killScroll);
    new MutationObserver(killScroll).observe(document.documentElement, {childList: true, subtree: true, attributes: true});
})();
</script>
"""

st.set_page_config(
    page_title="Cyber Proofreader",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.markdown(HEADER_HTML, unsafe_allow_html=True)

url_col, btn_col = st.columns([5, 1], vertical_alignment="bottom")
with url_col:
    url = st.text_input(
        "Website URL",
        placeholder="https://www.gov.il",
    )
with btn_col:
    run_clicked = st.button("▶ ANALYZE", type="primary", use_container_width=True)

progress_slot = st.empty()
status_slot = st.empty()
log_slot = st.empty()

if "report" in st.session_state:
    report = st.session_state["report"]
    source_url = st.session_state.get("source_url", "")

    if "language" in report:
        lang = report["language"]
        model = report.get("model", "—")
        st.markdown("### ◈ SCAN SUMMARY")

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(
                f'<div class="metric-card"><div class="value">{lang["name"]}</div>'
                f'<div class="label">Language ({lang["confidence"]:.0%})</div></div>',
                unsafe_allow_html=True,
            )
        with m2:
            st.markdown(
                f'<div class="metric-card"><div class="value" style="font-size:1rem;">'
                f'{model}</div><div class="label">Selected Model</div></div>',
                unsafe_allow_html=True,
            )

        total_chars = sum(
            int(p.get("char_count", 0))
            for k, p in report.items()
            if isinstance(p, dict) and "char_count" in p
        )
        total_issues = sum(
            int(p.get("issue_count", 0))
            for k, p in report.items()
            if isinstance(p, dict) and "issue_count" in p
        )
        with m3:
            st.markdown(
                f'<div class="metric-card"><div class="value">{total_chars:,}</div>'
                f'<div class="label">Characters</div></div>',
                unsafe_allow_html=True,
            )
        with m4:
            st.markdown(
                f'<div class="metric-card"><div class="value">{total_issues}</div>'
                f'<div class="label">Issues Found</div></div>',
                unsafe_allow_html=True,
            )

        selection = report.get("model_selection")
        if selection and selection.get("benchmarks"):
            st.markdown("### ◈ MODEL BENCHMARK")
            rows = []
            for b in selection["benchmarks"]:
                rows.append({
                    "Model": b["model"],
                    "Installed": "✓" if b["installed"] else "✗",
                    "Valid JSON": "✓" if b["valid_json"] else "✗",
                    "Time (s)": b["latency_seconds"],
                    "Score": b["total_score"],
                })
            st.dataframe(rows, use_container_width=True, hide_index=True)
            if selection.get("rationale"):
                st.info(selection["rationale"])

    st.markdown("### ◈ FINDINGS LOG")
    for page_url, page_data in report.items():
        if page_url in METADATA_KEYS:
            continue
        if not isinstance(page_data, dict):
            continue

        st.markdown(f"#### [{page_url}]({page_url})")
        if "error" in page_data:
            st.error(page_data["error"])
            continue

        issues = page_data.get("issues", [])
        if not issues:
            st.success("No issues found.")
            continue

        table_rows = []
        for issue in issues:
            label, _ = ISSUE_TYPE_LABELS.get(issue["type"], (issue["type"], ""))
            table_rows.append({
                "Type": label,
                "Original": issue.get("original", ""),
                "Suggestion": issue.get("suggestion") or "—",
                "Reason": issue.get("reason") or "—",
            })
        st.dataframe(table_rows, use_container_width=True, hide_index=True)

    if "language" in report:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", delete=False, encoding="utf-8"
        ) as tmp:
            write_html_report(tmp.name, report, source_url)
            html_bytes = Path(tmp.name).read_bytes()

        st.download_button(
            label="⬇ EXPORT HTML REPORT",
            data=html_bytes,
            file_name="report.html",
            mime="text/html",
        )

st.markdown("#### ◈ CONFIG PANEL")
st.caption("SETTINGS")

opt1, opt2, opt3, opt4 = st.columns(4)
with opt1:
    with st.container(border=True):
        st.markdown('<p class="config-section">▸ SCAN RANGE</p>', unsafe_allow_html=True)
        max_pages = st.number_input(
            "Max pages to crawl",
            min_value=1,
            max_value=MAX_PAGES,
            value=1,
            step=1,
            help="CLI: --max-pages N",
        )
with opt2:
    with st.container(border=True):
        st.markdown('<p class="config-section">▸ ANALYSIS MODE</p>', unsafe_allow_html=True)
        extract_only = st.checkbox(
            "Extract text only (no LLM)",
            value=False,
            help="CLI: --extract-only",
        )
        skip_benchmark = st.checkbox(
            "Skip model benchmark",
            value=False,
            help="CLI: --skip-benchmark",
        )
with opt3:
    with st.container(border=True):
        st.markdown('<p class="config-section">▸ MODEL OVERRIDE</p>', unsafe_allow_html=True)
        model_override = st.text_input(
            "Force model (optional)",
            placeholder=OLLAMA_MODEL,
            help="CLI: --model NAME",
            label_visibility="collapsed",
        )
        st.caption(f"default: {OLLAMA_MODEL}")
with opt4:
    with st.container(border=True):
        st.markdown('<p class="config-section">▸ TARGET LANG</p>', unsafe_allow_html=True)
        st.markdown("🇮🇱 Hebrew · 🇬🇧 English")
        st.caption("Export: HTML download (CLI: --html)")

if url.strip():
    flag_parts: list[str] = []
    if max_pages > 1:
        flag_parts.append(f"--max-pages {max_pages}")
    if extract_only:
        flag_parts.append("--extract-only")
    if skip_benchmark:
        flag_parts.append("--skip-benchmark")
    if model_override.strip():
        flag_parts.append(f'--model {model_override.strip()}')
    cli_preview = f"python main.py {url.strip()}"
    if flag_parts:
        cli_preview += " " + " ".join(flag_parts)
    with st.expander("Equivalent CLI command"):
        st.code(cli_preview, language="bash")

if run_clicked:
    if not url.strip():
        status_slot.error("Please enter a URL.")
    else:
        logs: list[str] = []

        def on_progress(update: ProgressUpdate) -> None:
            if update.percent is not None:
                progress_slot.progress(min(update.percent, 1.0))
            status_slot.markdown(f"**{update.stage.title()}** — {update.message}")
            logs.append(f"[{update.stage}] {update.message}")
            log_slot.code("\n".join(logs[-8:]), language=None)

        try:
            report = run_pipeline(
                url.strip(),
                max_pages=max_pages,
                extract_only=extract_only,
                model=model_override.strip() or None,
                skip_benchmark=skip_benchmark,
                on_progress=on_progress,
            )
            st.session_state["report"] = report
            st.session_state["source_url"] = url.strip()
            progress_slot.progress(1.0)
            status_slot.success("Done!")
        except SystemExit as exc:
            status_slot.error(str(exc) or "Ollama is not available. Start Ollama and pull a model.")
        except Exception as exc:
            status_slot.error(str(exc))

st.html(FOOTER_HTML, unsafe_allow_javascript=True)
