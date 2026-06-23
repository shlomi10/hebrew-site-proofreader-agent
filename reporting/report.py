import html
from datetime import datetime, timezone

TYPE_LABELS = {
    "spelling": "שגיאת כתיב",
    "grammar": "שגיאת דקדוק",
    "suspicious_phrasing": "ניסוח חשוד",
}

TYPE_CLASSES = {
    "spelling": "badge-spelling",
    "grammar": "badge-grammar",
    "suspicious_phrasing": "badge-suspicious",
}

TYPE_ICONS = {
    "spelling": "icon-spelling",
    "grammar": "icon-grammar",
    "suspicious_phrasing": "icon-suspicious",
}


def _esc(value: str) -> str:
    return html.escape(value or "")


def _icon(name: str) -> str:
    icons = {
        "report": """
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
          </svg>
        """,
        "pages": """
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <rect x="3" y="4" width="18" height="16" rx="2"/>
            <line x1="3" y1="9" x2="21" y2="9"/>
            <line x1="9" y1="4" x2="9" y2="20"/>
          </svg>
        """,
        "chars": """
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <polyline points="4 7 4 4 20 4 20 7"/>
            <line x1="9" y1="20" x2="15" y2="20"/>
            <line x1="12" y1="4" x2="12" y2="20"/>
          </svg>
        """,
        "issues": """
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
        """,
        "link": """
          <svg class="icon icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
            <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
          </svg>
        """,
        "spelling": """
          <svg class="icon icon-badge" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <path d="M12 20h9"/>
            <path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/>
          </svg>
        """,
        "grammar": """
          <svg class="icon icon-badge" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
          </svg>
        """,
        "suspicious": """
          <svg class="icon icon-badge" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
            <line x1="12" y1="9" x2="12" y2="13"/>
            <line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
        """,
        "ok": """
          <svg class="icon icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
            <polyline points="22 4 12 14.01 9 11.01"/>
          </svg>
        """,
        "error": """
          <svg class="icon icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <circle cx="12" cy="12" r="10"/>
            <line x1="15" y1="9" x2="9" y2="15"/>
            <line x1="9" y1="9" x2="15" y2="15"/>
          </svg>
        """,
        "clock": """
          <svg class="icon icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
        """,
        "meta-chars": """
          <svg class="icon icon-xs" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <line x1="17" y1="10" x2="3" y2="10"/>
            <line x1="21" y1="6" x2="3" y2="6"/>
            <line x1="21" y1="14" x2="3" y2="14"/>
            <line x1="17" y1="18" x2="3" y2="18"/>
          </svg>
        """,
        "meta-findings": """
          <svg class="icon icon-xs" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <path d="M14 2v6h6"/>
            <path d="M9 15l2 2 4-4"/>
          </svg>
        """,
    }
    return icons.get(name, "")


def _badge(issue_type: str, label: str) -> str:
    badge_class = TYPE_CLASSES.get(issue_type, "badge-default")
    icon_key = TYPE_ICONS.get(issue_type, "spelling")
    return (
        f'<span class="badge {badge_class}">'
        f'{_icon(icon_key)}<span>{_esc(label)}</span></span>'
    )


METADATA_KEYS = {"language", "model", "model_selection"}


def _page_entries(report: dict[str, object]) -> list[tuple[str, dict]]:
    return [
        (key, value)
        for key, value in report.items()
        if key not in METADATA_KEYS and isinstance(value, dict)
    ]


def build_html_report(report: dict[str, object], source_url: str) -> str:
    pages = _page_entries(report)
    total_issues = sum(
        int(page.get("issue_count", 0))
        for _, page in pages
        if "error" not in page
    )
    total_chars = sum(
        int(page.get("char_count", 0))
        for _, page in pages
        if "char_count" in page
    )
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    page_sections: list[str] = []

    for url, page_data in pages:
        if "error" in page_data:
            page_sections.append(
                f"""
                <section class="page-card">
                  <div class="page-header">
                    <h2>{_icon("link")}<a href="{_esc(url)}" target="_blank" rel="noopener">{_esc(url)}</a></h2>
                  </div>
                  <p class="error-box">{_icon("error")}<span>{_esc(str(page_data["error"]))}</span></p>
                </section>
                """
            )
            continue

        issues = page_data.get("issues", [])
        issue_rows: list[str] = []
        if issues:
            for issue in issues:
                if not isinstance(issue, dict):
                    continue
                issue_type = str(issue.get("type", ""))
                label = TYPE_LABELS.get(issue_type, issue_type)
                suggestion = issue.get("suggestion") or "—"
                reason = issue.get("reason") or "—"
                issue_rows.append(
                    f"""
                    <tr>
                      <td>{_badge(issue_type, label)}</td>
                      <td class="mono">{_esc(str(issue.get("original", "")))}</td>
                      <td class="mono">{_esc(str(suggestion))}</td>
                      <td>{_esc(str(reason))}</td>
                    </tr>
                    """
                )
            issues_html = f"""
            <div class="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>{_icon("issues")}<span>סוג</span></th>
                    <th>{_icon("chars")}<span>טקסט מקורי</span></th>
                    <th>{_icon("spelling")}<span>הצעת תיקון</span></th>
                    <th>{_icon("grammar")}<span>הסבר</span></th>
                  </tr>
                </thead>
                <tbody>
                  {''.join(issue_rows)}
                </tbody>
              </table>
            </div>
            """
        else:
            issues_html = (
                f'<p class="ok-box">{_icon("ok")}'
                f"<span>לא נמצאו בעיות בקטע זה.</span></p>"
            )

        page_sections.append(
            f"""
            <section class="page-card">
              <div class="page-header">
                <h2>{_icon("link")}<a href="{_esc(url)}" target="_blank" rel="noopener">{_esc(url)}</a></h2>
                <div class="page-meta">
                  <span class="meta-pill">{_icon("meta-chars")}{int(page_data.get("char_count", 0)):,} תווים</span>
                  <span class="meta-pill meta-pill-alert">{_icon("meta-findings")}{int(page_data.get("issue_count", 0))} ממצאים</span>
                </div>
              </div>
              {issues_html}
            </section>
            """
        )

    return f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>דוח בדיקת אתר — {_esc(source_url)}</title>
  <style>
    :root {{
      --bg: #f4f6f9;
      --card: #ffffff;
      --text: #1a2332;
      --muted: #5c6b7a;
      --border: #e2e8f0;
      --accent: #2563eb;
      --accent-soft: #dbeafe;
      --spelling: #eff6ff;
      --spelling-border: #93c5fd;
      --spelling-text: #1d4ed8;
      --grammar: #fffbeb;
      --grammar-border: #fcd34d;
      --grammar-text: #b45309;
      --suspicious: #fef2f2;
      --suspicious-border: #fca5a5;
      --suspicious-text: #b91c1c;
      --ok: #ecfdf5;
      --ok-border: #6ee7b7;
      --ok-text: #047857;
      --error: #fef2f2;
      --error-border: #fca5a5;
      --error-text: #991b1b;
      --shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", Tahoma, Arial, sans-serif;
      background: linear-gradient(180deg, #eef2ff 0%, var(--bg) 220px);
      color: var(--text);
      line-height: 1.6;
    }}
    .icon {{
      width: 1.35rem;
      height: 1.35rem;
      flex-shrink: 0;
    }}
    .icon-sm {{
      width: 1.1rem;
      height: 1.1rem;
    }}
    .icon-xs {{
      width: 0.95rem;
      height: 0.95rem;
    }}
    .icon-badge {{
      width: 0.95rem;
      height: 0.95rem;
    }}
    .container {{
      max-width: 1100px;
      margin: 0 auto;
      padding: 32px 20px 48px;
    }}
    .hero {{
      display: flex;
      gap: 18px;
      align-items: flex-start;
      background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 28px 32px;
      box-shadow: var(--shadow);
      margin-bottom: 24px;
    }}
    .hero-icon {{
      width: 3.4rem;
      height: 3.4rem;
      border-radius: 16px;
      display: grid;
      place-items: center;
      background: var(--accent-soft);
      color: var(--accent);
    }}
    .hero-icon .icon {{
      width: 1.8rem;
      height: 1.8rem;
    }}
    .hero h1 {{
      margin: 0 0 8px;
      font-size: 1.9rem;
    }}
    .hero p {{
      margin: 0;
      color: var(--muted);
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
    }}
    .hero-source {{
      color: var(--text);
    }}
    .hero-time {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}
    .stat {{
      display: flex;
      gap: 14px;
      align-items: center;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 20px;
      box-shadow: var(--shadow);
    }}
    .stat-icon {{
      width: 3rem;
      height: 3rem;
      border-radius: 14px;
      display: grid;
      place-items: center;
      color: var(--accent);
      background: #f8fafc;
      border: 1px solid var(--border);
    }}
    .stat-icon-issues {{
      color: var(--suspicious-text);
      background: var(--suspicious);
      border-color: var(--suspicious-border);
    }}
    .stat .label {{
      color: var(--muted);
      font-size: 0.92rem;
      margin-bottom: 2px;
    }}
    .stat .value {{
      font-size: 1.9rem;
      font-weight: 700;
      line-height: 1.1;
    }}
    .page-card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 24px;
      margin-bottom: 20px;
      box-shadow: var(--shadow);
    }}
    .page-header {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      margin-bottom: 18px;
    }}
    .page-header h2 {{
      margin: 0;
      font-size: 1.1rem;
      word-break: break-all;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }}
    .page-header a {{
      color: var(--accent);
      text-decoration: none;
    }}
    .page-header a:hover {{
      text-decoration: underline;
    }}
    .page-meta {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }}
    .meta-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #f8fafc;
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 7px 12px;
      color: var(--muted);
      font-size: 0.9rem;
    }}
    .meta-pill-alert {{
      background: var(--suspicious);
      border-color: var(--suspicious-border);
      color: var(--suspicious-text);
    }}
    .table-wrap {{
      overflow-x: auto;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.95rem;
    }}
    th, td {{
      border-bottom: 1px solid var(--border);
      padding: 14px 12px;
      text-align: right;
      vertical-align: top;
    }}
    th {{
      background: #f8fafc;
      color: var(--muted);
      font-weight: 600;
    }}
    th span {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    tr:last-child td {{
      border-bottom: none;
    }}
    .mono {{
      font-family: Consolas, "Courier New", monospace;
      white-space: pre-wrap;
      word-break: break-word;
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border-radius: 999px;
      padding: 7px 12px;
      font-size: 0.84rem;
      font-weight: 700;
      white-space: nowrap;
      border: 1px solid transparent;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
    }}
    .badge-spelling {{
      background: var(--spelling);
      color: var(--spelling-text);
      border-color: var(--spelling-border);
    }}
    .badge-grammar {{
      background: var(--grammar);
      color: var(--grammar-text);
      border-color: var(--grammar-border);
    }}
    .badge-suspicious {{
      background: var(--suspicious);
      color: var(--suspicious-text);
      border-color: var(--suspicious-border);
    }}
    .badge-default {{
      background: #f3f4f6;
      color: #374151;
      border-color: #d1d5db;
    }}
    .ok-box, .error-box {{
      margin: 0;
      border-radius: 12px;
      padding: 14px 16px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 10px;
      border: 1px solid transparent;
    }}
    .ok-box {{
      background: var(--ok);
      color: var(--ok-text);
      border-color: var(--ok-border);
    }}
    .error-box {{
      background: var(--error);
      color: var(--error-text);
      border-color: var(--error-border);
    }}
    .footer {{
      margin-top: 28px;
      color: var(--muted);
      font-size: 0.9rem;
      text-align: center;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 8px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <section class="hero">
      <div class="hero-icon">{_icon("report")}</div>
      <div>
        <h1>דוח בדיקת כתיב וניסוח</h1>
        <p>
          <span>מקור: <strong class="hero-source">{_esc(source_url)}</strong></span>
          <span class="hero-time">{_icon("clock")}<span>נוצר ב-{generated_at}</span></span>
        </p>
      </div>
    </section>

    <section class="stats">
      <div class="stat">
        <div class="stat-icon">{_icon("pages")}</div>
        <div>
          <div class="label">עמודים שנבדקו</div>
          <div class="value">{len(report)}</div>
        </div>
      </div>
      <div class="stat">
        <div class="stat-icon">{_icon("chars")}</div>
        <div>
          <div class="label">סה״כ תווים</div>
          <div class="value">{total_chars:,}</div>
        </div>
      </div>
      <div class="stat">
        <div class="stat-icon stat-icon-issues">{_icon("issues")}</div>
        <div>
          <div class="label">סה״כ ממצאים</div>
          <div class="value">{total_issues}</div>
        </div>
      </div>
    </section>

    {''.join(page_sections)}

    <div class="footer">{_icon("report")}<span>נוצר אוטומטית על ידי Website Spelling Checker Agent</span></div>
  </div>
</body>
</html>"""


def write_html_report(path: str, report: dict[str, object], source_url: str) -> None:
    content = build_html_report(report, source_url)
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)
