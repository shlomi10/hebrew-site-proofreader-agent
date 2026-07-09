INTERACTIVE_CSS = """
.stButton > button,
button[data-testid="stBaseButton-primary"],
button[data-testid="stBaseButton-secondary"],
button[data-testid="stBaseButton-primaryFormSubmit"],
[data-testid="stBaseButton-primary"],
[data-testid="stBaseButton-secondary"] {
    background: rgba(255, 176, 0, 0.2) !important;
    background-color: rgba(255, 176, 0, 0.2) !important;
    border: 1px solid #ffc933 !important;
    color: #fff4cc !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border-radius: 4px !important;
    min-height: 2.75rem !important;
    box-shadow: 0 0 18px rgba(255, 176, 0, 0.38), inset 0 0 12px rgba(255, 176, 0, 0.1) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover,
button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="stBaseButton-secondary"]:hover {
    background: rgba(255, 176, 0, 0.32) !important;
    background-color: rgba(255, 176, 0, 0.32) !important;
    border-color: #ffd966 !important;
    color: #fff8dc !important;
    box-shadow: 0 0 28px rgba(255, 176, 0, 0.55), inset 0 0 16px rgba(255, 176, 0, 0.14) !important;
}

[data-testid="stTextInput"],
[data-testid="stNumberInput"],
.stTextInput,
.stNumberInput {
    background: rgba(255, 176, 0, 0.1) !important;
    border: 1px solid rgba(255, 176, 0, 0.55) !important;
    border-radius: 4px !important;
    padding: 0.2rem 0.35rem !important;
    box-shadow: inset 0 0 14px rgba(255, 176, 0, 0.1) !important;
}

[data-testid="stTextInput"] [data-baseweb="input"],
[data-testid="stNumberInput"] [data-baseweb="input"],
[data-testid="stTextInput"] [data-baseweb="base-input"],
[data-testid="stNumberInput"] [data-baseweb="base-input"],
div[data-baseweb="input"] {
    background: #142436 !important;
    background-color: #142436 !important;
    border: 1px solid rgba(255, 176, 0, 0.65) !important;
    border-radius: 4px !important;
    box-shadow: inset 0 0 10px rgba(255, 176, 0, 0.12) !important;
}

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
.stTextInput input,
.stNumberInput input {
    background: transparent !important;
    background-color: transparent !important;
    color: #ffe8a8 !important;
    border: none !important;
    min-height: 2.75rem !important;
    font-family: 'JetBrains Mono', monospace !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: rgba(255, 200, 80, 0.5) !important;
}

[data-testid="stTextInput"] [data-baseweb="input"]:focus-within,
[data-testid="stNumberInput"] [data-baseweb="input"]:focus-within {
    border-color: #ffd966 !important;
    box-shadow: 0 0 16px rgba(255, 176, 0, 0.4), inset 0 0 12px rgba(255, 176, 0, 0.14) !important;
}

[data-testid="stNumberInput"] button {
    background: rgba(255, 176, 0, 0.22) !important;
    background-color: rgba(255, 176, 0, 0.22) !important;
    border: 1px solid rgba(255, 176, 0, 0.65) !important;
    color: #ffe8a8 !important;
}

[data-testid="stNumberInput"] button:hover {
    background: rgba(255, 176, 0, 0.34) !important;
    background-color: rgba(255, 176, 0, 0.34) !important;
    border-color: #ffd966 !important;
    color: #fff4cc !important;
}

[data-testid="stCheckbox"],
[data-testid="stCheckbox"] label {
    background: rgba(255, 176, 0, 0.08) !important;
    border: 1px solid rgba(255, 176, 0, 0.45) !important;
    border-radius: 4px !important;
    padding: 0.2rem 0.4rem !important;
    margin-bottom: 0.2rem !important;
    box-shadow: inset 0 0 10px rgba(255, 176, 0, 0.06) !important;
}

[data-testid="stCheckbox"] label span,
[data-testid="stCheckbox"] label p,
[data-testid="stCheckbox"] label div {
    color: #ffe8a8 !important;
}

[data-testid="stCheckbox"] input[type="checkbox"] {
    accent-color: #ffb000 !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] details {
    background: rgba(255, 176, 0, 0.1) !important;
    border: 1px solid rgba(255, 176, 0, 0.45) !important;
    border-radius: 4px !important;
    color: #ffe8a8 !important;
}

[data-testid="stExpander"] summary:hover {
    background: rgba(255, 176, 0, 0.18) !important;
    border-color: #ffd966 !important;
}

div[data-testid="stHorizontalBlock"]:has([data-testid="stTextInput"]) {
    align-items: flex-end !important;
}

div[data-testid="stHorizontalBlock"]:has([data-testid="stTextInput"]) [data-testid="column"]:last-child .stButton {
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Orbitron:wght@500;700&display=swap');

:root {
    --cyber-bg: #050810;
    --cyber-panel: #0a1018;
    --cyber-border: #00fff9;
    --cyber-green: #00ff41;
    --cyber-magenta: #ff2bd6;
    --cyber-amber: #ffb000;
    --cyber-text: #c8f4ff;
    --cyber-dim: #5a7a8a;
    --cyber-interactive-bg: #142436;
    --cyber-interactive-border: #ffb000;
    --cyber-interactive-glow: rgba(255, 176, 0, 0.28);
}

.stApp {
    background-color: var(--cyber-bg);
    background-image:
        linear-gradient(rgba(0, 255, 249, 0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 255, 249, 0.04) 1px, transparent 1px);
    background-size: 28px 28px;
    height: 100vh !important;
    max-height: 100vh !important;
    overflow: hidden !important;
}

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
    color: var(--cyber-text);
    overflow: hidden !important;
    height: 100% !important;
    max-height: 100% !important;
    margin: 0 !important;
}

body {
    position: fixed !important;
    inset: 0 !important;
    width: 100% !important;
}

[data-testid="stAppViewContainer"] {
    background: transparent;
    height: 100vh !important;
    max-height: 100vh !important;
    overflow: hidden !important;
}

section.main,
[data-testid="stMain"] {
    margin-left: 0 !important;
    padding-left: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
    height: 100vh !important;
    max-height: 100vh !important;
    overflow: hidden !important;
}

.block-container {
    padding-top: 0.75rem !important;
    padding-bottom: 1.25rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    max-width: 100% !important;
    max-height: 100vh !important;
    overflow: hidden !important;
}

[data-testid="stVerticalBlock"] {
    gap: 0.35rem !important;
}

.main-header {
    background: linear-gradient(135deg, rgba(0, 255, 249, 0.08) 0%, rgba(255, 43, 214, 0.08) 100%);
    border: 1px solid var(--cyber-border);
    box-shadow: 0 0 16px rgba(0, 255, 249, 0.12), inset 0 0 24px rgba(0, 255, 249, 0.02);
    padding: 0.65rem 1rem;
    border-radius: 4px;
    margin-bottom: 0.65rem;
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--cyber-border), var(--cyber-magenta), transparent);
}

.main-header h1 {
    margin: 0;
    font-family: 'Orbitron', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--cyber-green);
    text-shadow: 0 0 12px rgba(0, 255, 65, 0.6);
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.main-header p {
    margin: 0.3rem 0 0;
    font-size: 0.7rem;
    color: var(--cyber-dim);
    letter-spacing: 0.03em;
}

.metric-card {
    background: var(--cyber-panel);
    border: 1px solid rgba(0, 255, 249, 0.35);
    border-radius: 4px;
    padding: 0.65rem;
    text-align: center;
    box-shadow: 0 0 12px rgba(0, 255, 249, 0.06);
}

.metric-card .value {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--cyber-green);
    text-shadow: 0 0 8px rgba(0, 255, 65, 0.4);
}

.metric-card .label {
    font-size: 0.72rem;
    color: var(--cyber-dim);
    margin-top: 0.35rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

section[data-testid="stSidebar"],
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
[data-testid="stSidebarNav"],
[data-testid="stSidebarUserContent"],
[data-testid="stSidebarCollapseButton"],
.stSidebar {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    min-width: 0 !important;
    max-width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
}

[data-testid="stAppViewContainer"] > section.main > div {
    max-width: 100% !important;
    max-height: 100vh !important;
    overflow: hidden !important;
}

.config-section {
    font-family: 'Orbitron', sans-serif !important;
    color: var(--cyber-green) !important;
    font-size: 0.65rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin: 0 0 0.35rem 0 !important;
    padding-bottom: 0.25rem;
    border-bottom: 1px solid rgba(0, 255, 65, 0.35);
    text-shadow: 0 0 8px rgba(0, 255, 65, 0.35);
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid rgba(0, 255, 249, 0.35) !important;
    background: rgba(0, 255, 249, 0.04) !important;
    box-shadow: 0 0 10px rgba(0, 255, 249, 0.06) !important;
    border-radius: 4px !important;
    padding: 0.45rem 0.55rem !important;
}

""" + INTERACTIVE_CSS + """

h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: var(--cyber-border) !important;
    letter-spacing: 0.06em;
    font-size: 0.95rem !important;
    margin-top: 0.5rem !important;
    margin-bottom: 0.35rem !important;
}

h4 {
    font-family: 'Orbitron', sans-serif !important;
    color: var(--cyber-border) !important;
    letter-spacing: 0.06em;
    font-size: 0.85rem !important;
    margin-top: 0.35rem !important;
    margin-bottom: 0.25rem !important;
}

[data-testid="stAlert"] {
    background: var(--cyber-panel) !important;
    border: 1px solid rgba(0, 255, 249, 0.25) !important;
}

div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--cyber-border), var(--cyber-magenta)) !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(0, 255, 249, 0.2);
    border-radius: 4px;
}

[data-testid="stHeader"], [data-testid="stToolbar"], header[data-testid="stHeader"] {
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    overflow: hidden !important;
    visibility: hidden !important;
    padding: 0 !important;
    margin: 0 !important;
}

html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], section.main, .main, .block-container, [data-testid="stVerticalBlock"], [data-testid="stBottom"], [data-testid="stBottomBlockContainer"] {
    overflow: hidden !important;
    overflow-y: hidden !important;
    overflow-x: hidden !important;
}

[data-testid="stHtml"], [data-testid="stHtml"] > div, .stHtml {
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    border: none !important;
}

* {
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
}

*::-webkit-scrollbar,
*::-webkit-scrollbar-thumb,
*::-webkit-scrollbar-track {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    background: transparent !important;
}
</style>
"""

HEADER_HTML = """
<div class="main-header">
    <h1>◈ CYBER PROOFREADER ARRAY ◈</h1>
    <p>// LOCAL SCAN · OFFLINE · HEBREW / ENGLISH</p>
</div>
"""

ISSUE_TYPE_LABELS = {
    "spelling": ("שגיאת כתיב", "issue-spelling"),
    "grammar": ("שגיאת דקדוק", "issue-grammar"),
    "suspicious_phrasing": ("ניסוח חשוד", "issue-suspicious"),
}

METADATA_KEYS = frozenset({"language", "model", "model_selection"})
