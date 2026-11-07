CodeGraph AI — Intelligent Python Code Search

CodeGraph AI is a Python-based project that helps developers locate relevant source files and understand their code using AI-powered explanations.

Features

* Python Code Search: Find source files relevant to natural-language questions.
* Gemini AI Integration: Generate explanations of search results using Google’s Gemini API.
* File Ranking: Identify and rank relevant Python files.
* Command-Line Interface: Run code searches directly from the terminal.
* Modular Architecture: Separate search, evaluation, and AI explanation components.

Technologies Used

* Python
* Google Gemini API
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

