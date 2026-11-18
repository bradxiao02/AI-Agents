# AI Chat Agent

A general-purpose AI chat assistant built with Python, Streamlit and Ollama. The agent combines a locally hosted language model with practical tools, conversation memory, input validation and automated tests.

## Features

- **AI Conversations:** Interact with a locally hosted Qwen 2.5 1.5B model.
- **Tool Integration:** Five registered tools for practical tasks.
- **Calculator:** Safely evaluates mathematical expressions.
- **Date and Time:** Retrieves current date and time.
- **Word Counter:** Counts words and characters.
- **Text Analyzer:** Analyzes text structure and common words.
- **Unit Converter:** Converts supported length and weight measurements.
- **Conversation Memory:** Saves and retrieves conversation history.
- **Streamlit Interface:** Provides an interactive web-based chat interface.
- **Input Validation:** Checks user input and enforces a 5,000-character limit.
- **Automated Testing:** Includes 25 passing tests covering tools, execution, memory and input security.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Ollama | Local AI model runtime |
| Qwen 2.5 1.5B | Language model |
| Streamlit | Web interface |
| Requests | Communication with Ollama API |
| SQLite | Used by individual tools if applicable |
| Pytest | Automated testing |
| JSON | Conversation memory storage |

## Project Structure

```text
ai-chat-agent/
│
├── src/
│   ├── agent.py
│   ├── app.py
│   └── tools.py
│
├── tests/
│   ├── test_execution.py
│   ├── test_memory.py
│   ├── test_security.py
│   └── test_tools.py
│
├── data/
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd ai-chat-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Install and configure Ollama

Download Ollama from:

https://ollama.com/

Pull the required model:

```bash
ollama pull qwen2.5:1.5b
```

Ensure Ollama is running before launching the application.

## Running the Application

From the project root:

```bash
python -m streamlit run src/app.py
```

Streamlit will provide a local address in your terminal. Open it in your browser.

## Running Tests

Execute the automated test suite:

```bash
python -m pytest -v
```

The current development version has successfully passed all 25 tests.

## Security Considerations

This project incorporates several defensive programming practices:

- Restricted mathematical expression evaluation.
- Input validation and length restrictions.
- Validation of tool names and arguments.
- Rejection of unexpected tool parameters.
- Controlled conversation-memory handling.
- Error handling for model and tool execution.

**Limitations:** System-prompt instructions are not a complete defence against prompt injection. Tool-selection decisions made by a small language model may also be inaccurate. This project is intended for learning and experimentation, not deployment as a production security-critical system.

## Future Improvements

- More advanced tool orchestration.
- Improved prompt-injection resistance.
- Streaming AI responses.
- Enhanced conversation management.
- Additional AI integrations.
- Docker-based deployment.
- More comprehensive security testing.

## Author

Bradxiao02

## License

This project is available for educational and portfolio purposes. A formal open-source license can be added when selected.
