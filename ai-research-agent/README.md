# AI Research Agent

An AI-powered research assistant that searches the web, retrieves information, analyses sources using a locally hosted language model, and generates structured research reports.

## Features

- **Web Research:** Searches the web using DuckDuckGo.
- **AI Analysis:** Uses Ollama and Qwen 2.5 to analyse retrieved information.
- **Research Modes:** General, Academic, Technical and Cybersecurity.
- **Source Citations:** Generates numbered citations and references.
- **Research History:** Stores reports locally using SQLite.
- **Report Management:** View, delete and regenerate previous research.
- **Report Export:** Download reports in PDF, DOCX and Markdown formats.
- **Interactive Interface:** Built with Streamlit.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| User Interface | Streamlit |
| AI Model Runtime | Ollama |
| Language Model | Qwen 2.5 (1.5B) |
| Web Search | DuckDuckGo Search |
| Web Scraping | BeautifulSoup |
| Database | SQLite |
| PDF Export | ReportLab |
| Word Export | python-docx |
| Testing | Pytest |

## Project Structure

```text
ai-research-agent/
│
├── src/
│   ├── agent.py
│   ├── citations.py
│   ├── exporter.py
│   ├── memory.py
│   ├── researcher.py
│   └── search.py
│
├── tests/
│   └── test_agent.py
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/bradxiao02/AI-Agents.git
cd AI-Agents/ai-research-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and start Ollama

Download Ollama from:

https://ollama.com/

Pull the required model:

```bash
ollama pull qwen2.5:1.5b
```

Ensure Ollama is running before starting the application.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## Running Tests

Run the test suite using:

```bash
python -m pytest -v
```

## How It Works

1. The user submits a research question.
2. The search module retrieves relevant web results.
3. The application attempts to retrieve full webpage content.
4. The researcher module sends the retrieved information to the local Qwen model.
5. The AI generates a structured research report with numbered citations.
6. The citations module generates the corresponding references.
7. The memory module saves the report in a local SQLite database.
8. The exporter module generates downloadable PDF and Word documents.

## Privacy and Limitations

- AI analysis runs locally through Ollama.
- Web searches require an internet connection.
- Retrieved webpage content may be incomplete or unavailable.
- Research quality depends on the relevance and reliability of retrieved sources.
- Research history is stored locally in SQLite.
- AI-generated findings should be independently verified before academic or professional use.

## Author

**GitHub:** [@bradxiao02](https://github.com/bradxiao02)

---