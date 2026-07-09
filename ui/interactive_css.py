INTERACTIVE_CSS = """
.stButton > button,
button[data-testid="stBaseButton-primary"],
button[data-testid="stBaseButton-secondary"],
button[data-testid="stBaseButton-primaryFormSubmit"],
[data-testid="stBaseButton-primary"],
[data-testid="stBaseButton-secondary"] {
    background: rgba(8, 28, 16, 0.92) !important;
    background-color: rgba(8, 28, 16, 0.92) !important;
    border: 1px solid rgba(0, 255, 65, 0.55) !important;
    color: #00ff41 !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border-radius: 2px !important;
    min-height: 2.75rem !important;
    box-shadow: 0 0 14px rgba(0, 255, 65, 0.22), inset 0 0 10px rgba(0, 255, 65, 0.04) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover,
button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="stBaseButton-secondary"]:hover {
    background: rgba(12, 40, 22, 0.95) !important;
    background-color: rgba(12, 40, 22, 0.95) !important;
    border-color: #00ff41 !important;
    color: #b8ffd0 !important;
    box-shadow: 0 0 22px rgba(0, 255, 65, 0.38), inset 0 0 14px rgba(0, 255, 65, 0.08) !important;
}

[data-testid="stTextInput"],
[data-testid="stNumberInput"],
.stTextInput,
.stNumberInput {
    background: rgba(0, 255, 65, 0.04) !important;
    border: 1px solid rgba(0, 255, 65, 0.35) !important;
    border-radius: 2px !important;
    padding: 0.2rem 0.35rem !important;
    box-shadow: inset 0 0 12px rgba(0, 255, 65, 0.05) !important;
}

[data-testid="stTextInput"] [data-baseweb="input"],
[data-testid="stNumberInput"] [data-baseweb="input"],
[data-testid="stTextInput"] [data-baseweb="base-input"],
[data-testid="stNumberInput"] [data-baseweb="base-input"],
div[data-baseweb="input"] {
    background: #0a1410 !important;
    background-color: #0a1410 !important;
    border: 1px solid rgba(0, 255, 249, 0.35) !important;
    border-radius: 2px !important;
    box-shadow: inset 0 0 10px rgba(0, 255, 249, 0.06) !important;
}

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
.stTextInput input,
.stNumberInput input {
    background: transparent !important;
    background-color: transparent !important;
    color: #00ff41 !important;
    border: none !important;
    min-height: 2.75rem !important;
    font-family: 'JetBrains Mono', monospace !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: rgba(0, 255, 65, 0.35) !important;
}

[data-testid="stTextInput"] [data-baseweb="input"]:focus-within,
[data-testid="stNumberInput"] [data-baseweb="input"]:focus-within {
    border-color: #00fff9 !important;
    box-shadow: 0 0 14px rgba(0, 255, 249, 0.28), inset 0 0 10px rgba(0, 255, 249, 0.08) !important;
}

[data-testid="stNumberInput"] button {
    background: rgba(8, 28, 16, 0.9) !important;
    background-color: rgba(8, 28, 16, 0.9) !important;
    border: 1px solid rgba(0, 255, 65, 0.45) !important;
    color: #00ff41 !important;
}

[data-testid="stNumberInput"] button:hover {
    background: rgba(12, 40, 22, 0.95) !important;
    background-color: rgba(12, 40, 22, 0.95) !important;
    border-color: #00ff41 !important;
    color: #b8ffd0 !important;
}

[data-testid="stCheckbox"],
[data-testid="stCheckbox"] label {
    background: rgba(0, 255, 65, 0.04) !important;
    border: 1px solid rgba(0, 255, 65, 0.28) !important;
    border-radius: 2px !important;
    padding: 0.2rem 0.4rem !important;
    margin-bottom: 0.2rem !important;
    box-shadow: inset 0 0 8px rgba(0, 255, 65, 0.04) !important;
}

[data-testid="stCheckbox"] label span,
[data-testid="stCheckbox"] label p,
[data-testid="stCheckbox"] label div {
    color: #7fd4a0 !important;
}

[data-testid="stCheckbox"] input[type="checkbox"] {
    accent-color: #00ff41 !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] details {
    background: rgba(0, 255, 65, 0.05) !important;
    border: 1px solid rgba(0, 255, 249, 0.3) !important;
    border-radius: 2px !important;
    color: #7fd4a0 !important;
}

[data-testid="stExpander"] summary:hover {
    background: rgba(0, 255, 65, 0.1) !important;
    border-color: #00fff9 !important;
}

div[data-testid="stHorizontalBlock"]:has([data-testid="stTextInput"]) {
    align-items: flex-end !important;
}

div[data-testid="stHorizontalBlock"]:has([data-testid="stTextInput"]) [data-testid="stColumn"]:last-child .stButton {
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}
"""
