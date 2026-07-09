# 🔍 Website Spelling Checker Agent

[GitHub](https://github.com/shlomi10/hebrew-site-proofreader-agent)
[Python](https://www.python.org/)
[Playwright](https://playwright.dev/python/)
[LangChain](https://www.langchain.com/)
[Ollama](https://ollama.com/)
[Hebrew]()
[Privacy]()

An automated agent that accepts a website URL, extracts user-visible text, and checks for spelling errors, grammar issues, and suspicious phrasing — using a **local** language model (Ollama). Run via **CLI** or **Streamlit GUI**. No site content is sent to external cloud services.

---

## 📑 Table of Contents

- [📋 Overview](#-overview)
  - [📌 מטרת הפרויקט](#-מטרת-הפרויקט)
- [⚡ Quick Start](#-quick-start)
- [🏗️ Architecture](#️-architecture)
- [📁 Project Structure](#-project-structure)
- [⚙️ Workflow](#️-workflow)
- [🧰 Technology Choices](#-technology-choices)
- [🌐 Language Detection](#-language-detection)
- [🤖 Model Selection](#-model-selection)
- [📦 Installation](#-installation)
- [🚀 Usage](#-usage)
- [📊 Report Format](#-report-format)
- [🔧 Configuration](#-configuration)
- [⚠️ Limitations and Future Improvements](#️-limitations-and-future-improvements)
- [🛠️ Troubleshooting](#️-troubleshooting)
- [💻 System Requirements](#-system-requirements)
- [👤 Author](#-author)

---

## 📋 Overview

### 📌 מטרת הפרויקט

<div dir="rtl" align="right">

פיתוח Agent אוטומטי שמקבל מהמשתמש כתובת של אתר אינטרנט, סורק עמודים באתר, מאתר טקסטים גלויים למשתמש, ובודק האם קיימות בהם שגיאות כתיב או ניסוחים חשודים.

ה-Agent חייב להשתמש במודל שפה לוקאלי שרץ על מחשב המפתח, ללא שליחת תוכן האתר לשירותי ענן חיצוניים.

יש לחבר מודל שרלוונטי לסוג הבעיה המתוארת — ולהסביר מדוע נבחר המודל המסוים.

ה-Agent ירוץ בעברית ובאנגלית, ויש לבצע השוואה מדעית של לפחות 6 מודלים שונים.

</div>

The system supports **Hebrew** and **English** websites. The pipeline:

1. 🌐 User provides a URL.
2. 🎭 **Playwright** opens the page in headless Chromium and extracts only **visible** text (no `script`, no hidden elements).
3. 🔤 **Language detection** identifies Hebrew or English (`langdetect` + script-ratio heuristics). Other languages are rejected with a clear message.
4. 🧪 **Model benchmark** compares 7 candidate models (6+ per language) installed in Ollama and picks the best fit.
5. ✂️ Text is split into chunks (due to model context limits).
6. 🧠 A **LangChain Agent** sends each chunk to the **selected Ollama model** (`localhost:11434`).
7. 📐 The model returns structured findings (JSON / Pydantic).
8. 📄 Results are shown as **JSON** in the terminal, a styled **HTML report**, or in the **Streamlit GUI**.

You can run the agent via **CLI** (URL on the command line) or **GUI** (URL entered in the browser at `http://localhost:8501`).

During analysis, progress bars show model benchmarking and chunk-by-chunk analysis in the terminal or GUI.

![Cyber Proofreader GUI — full interface](ui/assets/gui-cyber.png)

*Current cyber-themed GUI: URL + ▶ ANALYZE, config panel (scan range, analysis mode, model override, languages), live results after scan, HTML export.*

---

## ⚡ Quick Start

### Prerequisites


| Requirement  | Notes                                                                            |
| ------------ | -------------------------------------------------------------------------------- |
| Python 3.14+ | With `venv` support                                                              |
| Ollama       | [Download](https://ollama.com/download) — must be **running** (system tray icon) |
| Internet     | For crawling target websites (analysis stays 100% local)                         |
| ~4–8 GB RAM  | Depends on model size                                                            |


### Install (one time)

```powershell
git clone https://github.com/shlomi10/hebrew-site-proofreader-agent.git
cd hebrew-site-proofreader-agent

python -m venv venv
.\venv\Scripts\Activate.ps1        # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Install **Ollama**, open a **new terminal**, then pull at least one model:

```powershell
ollama pull aminadaven/dictalm2.0-instruct:q4_k_m   # Hebrew (recommended)
ollama pull llama3.2                                 # English + benchmark comparison
ollama list
```

### Run (every time)

Activate the virtual environment, then choose **CLI** or **GUI**:


| Mode    | Command                             | Where to enter URL                 |
| ------- | ----------------------------------- | ---------------------------------- |
| **CLI** | `python main.py https://www.gov.il` | Command line                       |
| **GUI** | `python main.py --gui`              | Browser at `http://localhost:8501` |


```powershell
.\venv\Scripts\Activate.ps1

# CLI — JSON output
python main.py https://www.gov.il

# CLI — HTML report
python main.py https://www.gov.il --html --open

# GUI — no URL needed in the command
python main.py --gui
```

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│  main.py (CLI)                    ui/app.py (Streamlit GUI)          │
│  python main.py <url> [flags]     python main.py --gui               │
│  URL on command line              URL entered in browser             │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │    runner.py    │
                    │  shared pipeline│
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌─────────────────┐  ┌──────────────┐   ┌─────────────────────┐
│  crawl/         │  │  crawl/      │   │  analysis/          │
│  extractor.py   │  │  crawler.py  │   │  ollama_client.py   │
│  Playwright     │  │  BFS crawl   │   │  Ollama health      │
└────────┬────────┘  └──────┬───────┘   └──────────┬──────────┘
         │                  │                      │
         └────────┬─────────┘                      │
                  ▼                                │
         ┌─────────────────┐                       │
         │  analysis/      │                       │
         │  language.py    │                       │
         │  detect he/en   │                       │
         └────────┬────────┘                       │
                  ▼                                │
         ┌──────────────────┐                      │
         │  analysis/       │                      │
         │  model_selector  │                      │
         │  benchmark 7 LLMs│                      │
         └────────┬─────────┘                      │
                  ▼                                │
         ┌─────────────────┐                       │
         │  analysis/      │                       │
         │  text_utils.py  │                       │
         │  chunk split    │                       │
         └────────┬────────┘                       │
                  ▼                                │
         ┌─────────────────┐◄──────────────────────┘
         │  analysis/      │
         │  agent.py       │
         │  LangChain Agent│
         │  + ChatOllama   │
         └────────┬────────┘
                  ▼
         ┌─────────────────┐
         │  analysis/      │
         │  schemas.py     │
         └────────┬────────┘
                  ▼
    ┌─────────────┴─────────────────────┐
    ▼                 ▼                 ▼
 CLI: JSON      CLI: report.html    GUI: live view
 (stdout)       reporting/report.py  + HTML download
```

### 🔄 Flow Diagram (Mermaid)

```mermaid
flowchart TD
    START{Entry point?}
    START -->|CLI| A[main.py — URL on command line]
    START -->|GUI| A2[ui/app.py — URL in browser]
    A --> R[runner.py — shared pipeline]
    A2 --> R
    R --> B{max-pages > 1?}
    B -->|no| C[crawl/extractor.py: Playwright]
    B -->|yes| D[crawl/crawler.py: BFS]
    D --> C
    C --> E{extract-only?}
    E -->|yes| F[Return extracted text]
    E -->|no| G[analysis/language.py: detect Hebrew or English]
    G --> G2{Supported language?}
    G2 -->|no| G3[Exit: unsupported language]
    G2 -->|yes| G4[analysis/ollama_client: check Ollama]
    G4 --> G5[analysis/model_selector: benchmark 7 models]
    G5 --> H[analysis/text_utils: split into chunks]
    H --> I[analysis/agent.py: analyze with selected model]
    I --> J[Merge findings]
    J --> K{Output mode?}
    K -->|CLI + --html| L[report.html]
    K -->|CLI default| M[JSON to terminal]
    K -->|GUI| N[Streamlit dashboard + download HTML]
```



### 🧩 Separation of Concerns


| Layer          | Responsibility                              |
| -------------- | ------------------------------------------- |
| **Entry**      | `main.py` (CLI) or `ui/app.py` (GUI)        |
| **Pipeline**   | `runner.py` — shared orchestration logic    |
| **Extraction** | Playwright — deterministic, no LLM          |
| **Analysis**   | LangChain + Ollama — reasoning on text only |
| **Output**     | JSON / HTML / Streamlit — presentation      |


The agent does **not** open a browser or crawl the web. It receives pre-extracted text and analyzes it. This keeps the design simple, transparent, and easy to debug.

---

## 📁 Project Structure

```
Agent/
├── main.py                 # CLI entry point
├── runner.py               # Shared pipeline (CLI + GUI)
├── config.py               # Global settings
├── crawl/                  # Web crawling & text extraction
│   ├── extractor.py        # Playwright visible text
│   └── crawler.py          # BFS multi-page crawl
├── analysis/               # LLM analysis
│   ├── agent.py            # LangChain Agent + Ollama
│   ├── language.py         # Hebrew / English detection
│   ├── model_selector.py   # 7-model benchmark & selection
│   ├── schemas.py          # Pydantic output models
│   ├── ollama_client.py    # Ollama health check
│   └── text_utils.py       # Text chunking
├── ui/                     # Streamlit GUI
│   ├── app.py              # GUI entry point
│   ├── styles.py           # CSS and UI constants
│   ├── assets/
│   │   └── gui-cyber.png   # GUI screenshot (README)
│   └── .streamlit/
│       └── config.toml     # Streamlit theme
├── reporting/              # Report generation
│   └── report.py           # HTML report builder
├── requirements.txt
└── README.md
```

---

## ⚙️ Workflow

### 1️⃣ Extraction (Playwright)

`crawl/extractor.py` launches headless Chromium, loads the URL, and runs in-page JavaScript to collect only **visible** text:

- Skips `script`, `style`, `noscript`, `svg`
- Skips elements with `display: none`, `visibility: hidden`, `opacity: 0`
- Normalizes whitespace

### 2️⃣ Crawling (optional)

`crawl/crawler.py` performs BFS within the same domain:

- Page limit (`MAX_PAGES` / `--max-pages`)
- Delay between requests (`CRAWL_DELAY_SECONDS`)
- URL normalization

Default: **single page only**.

### 3️⃣ Language detection

`analysis/language.py` runs after extraction:

1. Computes Hebrew vs. Latin character ratios on the extracted text
2. If one script dominates (≥ 55%), classifies accordingly
3. Otherwise uses `langdetect` on a sample (up to 5,000 chars)
4. Returns language code, name, and confidence


| Result          | Action                                   |
| --------------- | ---------------------------------------- |
| `he` (Hebrew)   | Continue with Hebrew model catalog       |
| `en` (English)  | Continue with English model catalog      |
| Other / unknown | Exit with `Unsupported language` message |


### 4️⃣ Model benchmark & selection

`analysis/model_selector.py` compares **7 candidate models** per language (6+ as required):

1. Lists models installed in Ollama
2. Runs a live proofreading benchmark on a ~400-char sample from the extracted text
3. Scores each installed candidate (see [Scoring formula](#scoring-formula))
4. Prints a comparison table and rationale to stderr
5. Selects the highest-scoring installed model for full analysis

Models not installed appear in the table with a prior-only score and a `not installed` note.

### 5️⃣ Analysis (Agent + Ollama)

`analysis/agent.py`:

1. Splits text into ~800-character chunks (`TEXT_CHUNK_SIZE`)
2. Creates a LangChain Agent with `ChatOllama` using the **selected model**
3. Uses a **language-specific system prompt** (Hebrew or English)
4. Sends each chunk to detect:
  - Spelling errors
  - Grammar issues
  - Suspicious phrasing (phishing tone, excessive urgency, etc.)
5. Receives structured output (`TextAnalysisResult`)
6. Merges findings across chunks and deduplicates
7. Shows a **tqdm progress bar** while processing chunks

### 6️⃣ Report

- **CLI + JSON** — default, printed to terminal
- **CLI + HTML** — with `--html`, saved to `report.html` (RTL, Hebrew labels)
- **GUI** — live dashboard in the browser with summary cards, benchmark table, findings, and HTML download

---

## 🧰 Technology Choices


| Technology     | Role                | Why                                                    |
| -------------- | ------------------- | ------------------------------------------------------ |
| **Playwright** | Text extraction     | Renders JavaScript (SPAs), extracts truly visible text |
| **LangChain**  | Agent framework     | Ollama integration, structured Pydantic output         |
| **Ollama**     | Local LLM runtime   | Easy setup, localhost API, no cloud                    |
| **Pydantic**   | Output schema       | Validates `type`, `original`, `suggestion`, `reason`   |
| **httpx**      | Ollama health check | Verifies the local server before analysis              |
| **tqdm**       | Progress bar        | Shows benchmark and analysis progress                  |
| **langdetect** | Language detection  | Identifies Hebrew vs. English from extracted text      |
| **Streamlit**  | Web GUI             | Browser interface — URL, settings, live results        |


---

## 🌐 Language Detection

Supported: **Hebrew** and **English** only. All other languages are rejected.

After Playwright extracts text, `analysis/language.py` determines whether the content is Hebrew or English.

### How it works


| Step | Method       | Details                                                      |
| ---- | ------------ | ------------------------------------------------------------ |
| 1    | Script ratio | Counts Hebrew (U+0590–U+05FF) vs. Latin (A–Z) characters     |
| 2    | Threshold    | If one script ≥ 55% of letters → that language wins          |
| 3    | Fallback     | `langdetect` on up to 5,000 characters with confidence score |
| 4    | Gate         | Only `he` and `en` proceed; all other languages are rejected |


### Unsupported language example

```text
Unsupported language: fr (fr).
This agent supports Hebrew and English only.
```

---

## 🤖 Model Selection

The agent does **not** use a fixed model for every site. After language detection it runs a **scientific comparison** of at least **6 models** (7 in the catalog) and picks the best one for the detected language.

### Candidate models

#### Hebrew catalog (7 models)


| Model                                           | Prior (max 30) | Specialty                        |
| ----------------------------------------------- | -------------- | -------------------------------- |
| DictaLM `aminadaven/dictalm2.0-instruct:q4_k_m` | 30             | Hebrew-specialized LM by Dicta   |
| Llama `llama3.2`                                | 18             | Strong general multilingual      |
| Mistral `mistral`                               | 16             | Efficient European multilingual  |
| Qwen `qwen2.5`                                  | 17             | Strong reasoning, many languages |
| Gemma `gemma2`                                  | 15             | Compact Google model             |
| Phi `phi3`                                      | 12             | Small Microsoft model            |
| Aya `aya`                                       | 14             | Cohere multilingual              |


#### English catalog (7 models)


| Model                  | Prior (max 30) | Specialty                           |
| ---------------------- | -------------- | ----------------------------------- |
| Llama `llama3.2`       | 28             | Top English instruction following   |
| Llama `llama3.1`       | 27             | Large context, excellent English    |
| Mistral `mistral`      | 26             | Speed + English accuracy            |
| Qwen `qwen2.5`         | 27             | High English benchmark scores       |
| Gemma `gemma2`         | 25             | Good English, low VRAM              |
| Phi `phi3`             | 22             | Practical on modest hardware        |
| DeepSeek `deepseek-r1` | 24             | Deep reasoning for complex phrasing |


### Scoring formula

Each **installed** model is benchmarked on a real text sample (~400 chars). Total score is up to **65 points**:


| Component   | Max points | What is measured                            |
| ----------- | ---------- | ------------------------------------------- |
| **Prior**   | 30         | Language fit based on model specialization  |
| **JSON**    | 20         | Valid structured `{"errors": [...]}` output |
| **Latency** | 15         | Response time (faster = higher score)       |


Uninstalled models appear in the table with prior × 0.3 only and `not installed`.

### Why DictaLM for Hebrew?

DictaLM 2.0 Instruct is the **only model trained specifically on Hebrew corpora** (spelling, grammar, phrasing). General models like Llama or Mistral understand Hebrew but are less accurate for proofreading Hebrew websites. The live benchmark confirms this — DictaLM typically wins on Hebrew sites when installed.

```python
OLLAMA_MODEL = "aminadaven/dictalm2.0-instruct:q4_k_m"  # fallback default in config.py
```

### Why Llama 3.2 / Qwen 2.5 for English?

English sites need models trained on large English datasets with reliable JSON output. DictaLM is Hebrew-specialized and underperforms on English. Llama 3.2 and Qwen 2.5 consistently score highest in the English benchmark.

### Benchmark output (terminal)

```text
Detected language: Hebrew (confidence: 87%)
Running model benchmark (6+ candidates)...
Benchmarking models: 100%|████████| 3/3

שפה שזוהתה: עברית
מודל נבחר: aminadaven/dictalm2.0-instruct:q4_k_m
הסבר: DictaLM 2.0 אומן במיוחד על קורפוס עברי... Benchmark score: 58.2/65 ...

השוואה מדעית (7 מודלים בקטלוג, 3 מותקנים ונבדקו):
מודל                                     מותקן    JSON   זמן      ציון
aminadaven/dictalm2.0-instruct:q4_k_m    כן       כן     8.42     58.2
llama3.2                                 כן       כן     4.15     46.8
mistral                                  לא       לא     0.0      4.8
```

### Install models for full comparison

```powershell
ollama pull aminadaven/dictalm2.0-instruct:q4_k_m
ollama pull llama3.2
ollama pull mistral
ollama pull qwen2.5
ollama pull gemma2
ollama pull phi3
```

Only installed models are benchmarked live. With one model installed, that model is selected automatically.

### Manual override


| Flag               | Behavior                                            |
| ------------------ | --------------------------------------------------- |
| `--model NAME`     | Skip benchmark, use the specified Ollama model      |
| `--skip-benchmark` | Skip benchmark, use `OLLAMA_MODEL` from `config.py` |


**Why a local model?** Site content never leaves the developer machine.

---

## 📦 Installation

Full step-by-step guide. For a shorter version, see [Quick Start](#-quick-start).

### Step 1 — Clone the repository

```powershell
git clone https://github.com/shlomi10/hebrew-site-proofreader-agent.git
cd hebrew-site-proofreader-agent
```

### Step 2 — Python environment

Requires **Python 3.14+**.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1        # Windows
# source venv/bin/activate          # macOS / Linux

pip install -r requirements.txt
playwright install chromium
```

### Step 3 — Install Ollama

1. Download from [https://ollama.com/download](https://ollama.com/download)
2. Install and open a **new terminal**
3. Verify Ollama is running (system tray icon on Windows)

### Step 4 — Pull models

At least **one model** is required. For full benchmark comparison, pull several:

```powershell
# Hebrew (recommended for Israeli sites)
ollama pull aminadaven/dictalm2.0-instruct:q4_k_m

# English + general fallback
ollama pull llama3.2

# Optional — for fuller benchmark comparison
ollama pull mistral
ollama pull qwen2.5
ollama pull gemma2
ollama pull phi3

ollama list
```

### Step 5 — Verify setup

```powershell
.\venv\Scripts\Activate.ps1
python main.py https://example.com --extract-only
```

If text is extracted successfully, the environment is ready.

### Ollama install locations (optional)

- **Ollama app:** `%LOCALAPPDATA%\Programs\Ollama` (Windows)
- **Downloaded models:** `%USERPROFILE%\.ollama`

To store models on another drive:

```powershell
setx OLLAMA_MODELS "D:\ollama-models"
```

Restart Ollama after changing this variable.

---

## 🚀 Usage

Activate the virtual environment before every session:

```powershell
.\venv\Scripts\Activate.ps1
```

### Option A — CLI (command line)

The URL is passed as an argument.

#### Extract text only (no LLM)

```powershell
python main.py https://ynet.co.il --extract-only
```

#### Full analysis — JSON (auto language + model selection)

```powershell
python main.py https://www.gov.il
python main.py https://example.com
```

#### Full analysis — HTML report

```powershell
python main.py https://www.gov.il --html
python main.py https://www.gov.il --html --open
```

Output file: `report.html` in the project directory.

#### Crawl multiple pages

```powershell
python main.py https://example.co.il --max-pages 5 --html
```

#### Force a specific model (skip benchmark)

```powershell
python main.py https://www.gov.il --model llama3.2
```

#### Skip benchmark (use config default)

```powershell
python main.py https://www.gov.il --skip-benchmark
```

### Option B — GUI (browser interface)

No URL in the command — enter it in the browser.

```powershell
python main.py --gui
```

Or directly:

```powershell
cd ui
streamlit run app.py
```

Opens `http://localhost:8501` — cyber-themed single-page dashboard (see [Overview](#-overview) screenshot).

| Area | What you get |
| ---- | ------------ |
| **Top** | URL field + **▶ ANALYZE** button |
| **Config panel** | Max pages, extract-only, skip benchmark, model override, target languages |
| **After scan** | Summary cards, model benchmark table, findings per page |
| **Export** | Download styled HTML report |

- Live progress bar and status log during analysis
- Summary cards (language, model, characters, issues)
- Model benchmark table
- Findings table per page
- **Export HTML Report** button
- Footer: `100% local — offline node`

### CLI flags


| Flag               | Description                                              |
| ------------------ | -------------------------------------------------------- |
| `url`              | Website URL (required for CLI, not for `--gui`)          |
| `--gui`            | Launch Streamlit GUI (no URL needed)                     |
| `--extract-only`   | Playwright only, skip Ollama                             |
| `--max-pages N`    | Number of pages to crawl (default: 1)                    |
| `--html [FILE]`    | Save HTML report (default: `report.html`)                |
| `--open`           | Open the HTML report in the browser                      |
| `--model NAME`     | Use a specific Ollama model, skip benchmark              |
| `--skip-benchmark` | Use `OLLAMA_MODEL` from `config.py` without benchmarking |


---

## 📊 Report Format

### JSON

```json
{
  "language": {
    "code": "he",
    "name": "Hebrew",
    "confidence": 0.87
  },
  "model": "aminadaven/dictalm2.0-instruct:q4_k_m",
  "model_selection": {
    "model": "aminadaven/dictalm2.0-instruct:q4_k_m",
    "language": "he",
    "rationale": "DictaLM 2.0 אומן במיוחד על קורפוס עברי...",
    "candidates_compared": 3,
    "benchmarks": [
      {
        "model": "aminadaven/dictalm2.0-instruct:q4_k_m",
        "catalog_name": "aminadaven/dictalm2.0-instruct:q4_k_m",
        "total_score": 58.2,
        "installed": true,
        "valid_json": true,
        "latency_seconds": 8.42
      }
    ]
  },
  "https://ynet.co.il": {
    "char_count": 70517,
    "issue_count": 2,
    "issues": [
      {
        "type": "spelling",
        "original": "טקסט שגוי",
        "suggestion": "טקסט מתוקן",
        "reason": "שגיאת כתיב"
      },
      {
        "type": "suspicious_phrasing",
        "original": "לחצו עכשיו!!!",
        "suggestion": "",
        "reason": "ניסוח דחיפות חשוד"
      }
    ]
  }
}
```

### Issue types (`type`)


| Badge      | Value                 | Meaning                                                 |
| ---------- | --------------------- | ------------------------------------------------------- |
| spelling   | `spelling`            | Spelling error                                          |
| grammar    | `grammar`             | Grammar / phrasing issue                                |
| suspicious | `suspicious_phrasing` | Suspicious tone (phishing, urgency, unrealistic claims) |


### HTML report

- RTL layout with Hebrew labels
- SVG icons for hero, summary stats, page headers, and table columns
- Color-coded badges with icons per issue type (spelling, grammar, suspicious)
- Summary cards: pages, characters, findings
- Per-page table with styled meta pills
- Generated by `reporting/report.py` (CLI) or downloadable from the GUI

---

## 🔧 Configuration

`config.py`:


| Variable              | Badge  | Default                                 | Description                                  |
| --------------------- | ------ | --------------------------------------- | -------------------------------------------- |
| `OLLAMA_BASE_URL`     | ollama | `http://localhost:11434`                | Ollama server URL                            |
| `OLLAMA_MODEL`        | model  | `aminadaven/dictalm2.0-instruct:q4_k_m` | Fallback model when using `--skip-benchmark` |
| `MAX_PAGES`           | pages  | `20`                                    | Max pages when crawling                      |
| `CRAWL_DELAY_SECONDS` | delay  | `0.5`                                   | Delay between page requests                  |
| `TEXT_CHUNK_SIZE`     | chunk  | `800`                                   | Characters per analysis chunk                |


---

## ⚠️ Limitations and Future Improvements


| Limitation          | Badge | Notes                                                          |
| ------------------- | ----- | -------------------------------------------------------------- |
| **Benchmark time**  | bench | First run benchmarks each installed model (~seconds per model) |
| **Large sites**     | slow  | ynet (~70K chars) = many model calls — slow                    |
| **Accuracy**        | llm   | LLMs can produce false positives or miss errors                |
| **Dynamic content** | js    | Playwright handles JS; complex sites may need longer waits     |


### Possible improvements

- `--max-chars` to cap analyzed text length
- Filter repeated content (nav, footers)
- `robots.txt` check before crawling

---

## 🛠️ Troubleshooting


| Problem                                    | Badge    | Solution                                                  |
| ------------------------------------------ | -------- | --------------------------------------------------------- |
| `Unsupported language`                     | lang     | Only Hebrew and English sites are supported               |
| `Could not detect language`                | detect   | Page has too little text to classify                      |
| `ollama is not recognized`                 | install  | Install Ollama and open a new terminal                    |
| `Ollama is not running`                    | start    | Start Ollama from the system tray                         |
| `Model is not installed`                   | pull     | `ollama pull aminadaven/dictalm2.0-instruct:q4_k_m`       |
| `pull model manifest: file does not exist` | name     | Wrong model name — use the full name above                |
| `ModuleNotFoundError: langchain`           | pip      | `pip install -r requirements.txt` inside venv             |
| Playwright errors                          | chromium | `playwright install chromium`                             |
| `streamlit is not recognized`              | pip      | `pip install streamlit` inside venv                       |
| GUI does not open                          | gui      | `python main.py --gui` or `cd ui && streamlit run app.py` |


---

## 💻 System Requirements

Python
OS
RAM
Network
Analysis

- Python 3.14+
- Windows / macOS / Linux
- Ollama installed and running
- ~4–8 GB RAM (depends on model quantization)
- Internet for crawling the target site (analysis stays local)

---

## 👤 Author

**Shlomi Gross** — built this project as a local AI agent for proofreading Hebrew website content.

[Repository](https://github.com/shlomi10/hebrew-site-proofreader-agent)

**Repository:** [github.com/shlomi10/hebrew-site-proofreader-agent](https://github.com/shlomi10/hebrew-site-proofreader-agent)