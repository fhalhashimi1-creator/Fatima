CodeGraph AI — Intelligent Python Code Search

CodeGraph AI is a Python-based project that helps developers locate relevant source files and understand their code using AI-powered explanations.

Features

* Python Code Search: Find source files relevant to natural-language questions.
* Local AI Integration: Generate AI-powered explanations using Gemma 3:1b through Ollama and an OpenAI-compatible API.
* File Ranking: Identify and rank relevant Python files.
* Command-Line Interface: Run code searches directly from the terminal.
* Modular Architecture: Separate search, evaluation, and AI explanation components.

Technologies Used

* Python
* Gemma 3:1b (Local AI Model)
* Ollama (Local AI Runtime)
* OpenAI-Compatible REST API
* REST APIs
* JSON
* Git and GitHub

Project Structure

* core.py — Code search and indexing
* agent.py — AI-powered explanations
* evaluate.py — Evaluation functionality
* __main__.py — Command-line entry point
* __init__.py — Python package initialization

Example Usage

Run the following command from the repository root:

python -m codegraph.Codegraph . "Which files handle code search?"

CodeGraph returns relevant files and can generate AI explanations when Gemini is configured.

Security

API keys are supplied through environment variables and must never be committed to GitHub.

Future Improvements

* Web-based user interface
* Support for additional programming languages
* Improved code search accuracy
* Interactive AI code assistant

Project Purpose

This project demonstrates practical skills in Python programming, API integration, AI-assisted development, code search, and software engineering.


## Local AI Setup (Gemma 3)

CodeGraph AI supports local AI-powered explanations using Ollama and Gemma 3:1b.

### 1. Install Ollama
Visit https://ollama.com to install Ollama.

### 2. Download the AI Model
```bash
ollama pull gemma3:1b
```

### 3. Start Ollama
```bash
ollama serve
```

### 4. Configure CodeGraph AI
In a separate terminal, run:

```bash
export CODEGRAPH_LLM_URL="http://localhost:11434/v1/chat/completions"
export CODEGRAPH_LLM_MODEL="gemma3:1b"
```

### 5. Run CodeGraph AI
From the repository root:

```bash
python -m codegraph.Codegraph . "Where is the search function implemented?" --explain
```

The output includes relevant source files and an AI-generated explanation when the model is available.

### Run Automated Tests
```bash
python -m unittest discover -s tests -v
```

The automated tests use mocked AI responses and do not require Ollama to be running.
