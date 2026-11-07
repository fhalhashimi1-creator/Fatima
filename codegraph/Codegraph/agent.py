"""Optional Gemma inference via a user-supplied OpenAI-compatible endpoint."""
from __future__ import annotations
import json
import os
from urllib.request import Request, urlopen
from .core import search


def explain(index: dict, query: str, *, endpoint: str | None = None, model: str | None = None, limit: int = 5) -> dict:
    """Retrieve candidates and optionally ask a configured model to explain them.

    This function never claims an LLM was run when no endpoint is configured.
    Configure CODEGRAPH_LLM_URL (full chat/completions URL), CODEGRAPH_LLM_MODEL,
    and optionally CODEGRAPH_LLM_KEY. Keep the endpoint trusted: code paths are
    sent to that endpoint, so do not use it for confidential repositories.
    """
    candidates = search(index, query, limit=limit)
    result = {'query': query, 'candidates': candidates, 'model_used': False, 'explanation': None}
    endpoint = endpoint or os.getenv('CODEGRAPH_LLM_URL')
    model = model or os.getenv('CODEGRAPH_LLM_MODEL')
    if not endpoint or not model:
        return result
    if not endpoint.startswith(('https://', 'http://localhost:', 'http://127.0.0.1:')):
        raise ValueError('Use HTTPS or a localhost endpoint')
    prompt = ('Question: ' + query + '\nCandidate files (from static import graph):\n' +
              json.dumps(candidates, indent=2) + '\nExplain which files to inspect first. '
              'Do not claim to have read file bodies or fixed the bug. '
              'State uncertainty where appropriate.')
    body = json.dumps({'model': model, 'temperature': 0, 'messages': [
        {'role': 'system', 'content': 'You are a cautious repository navigation assistant. Only use supplied evidence.'},
        {'role': 'user', 'content': prompt}
    ]}).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    if os.getenv('CODEGRAPH_LLM_KEY'):
        headers['Authorization'] = 'Bearer ' + os.environ['CODEGRAPH_LLM_KEY']
    req = Request(endpoint, data=body, headers=headers, method='POST')
    with urlopen(req, timeout=60) as response:
        data = json.load(response)
    result['explanation'] = data['choices'][0]['message']['content']
    result['model_used'] = True
    result['model_name'] = model
    return result
