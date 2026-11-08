"""Repository indexing and graph-aware retrieval for Python projects."""
from __future__ import annotations
import ast
import json
import re
from collections import deque
from pathlib import Path

STOPWORDS = {'the','a','an','is','in','on','of','for','to','and','or','why','how','my','with','not','does','are','file','code','error','bug','fix'}


def tokens(value: str) -> set[str]:
    return {t for t in re.findall(r'[a-z][a-z0-9]*', re.sub(r'([a-z])([A-Z])', r'\1 \2', value).lower()) if t not in STOPWORDS}


def build_index(root: str | Path) -> dict:
    root = Path(root).resolve()
    paths = sorted(p for p in root.rglob('*.py') if p.is_file() and not any(x in {'.git','.venv','venv','__pycache__'} for x in p.relative_to(root).parts))
    modules = {}
    for p in paths:
        rel = p.relative_to(root).as_posix()
        mod = '.'.join(p.relative_to(root).with_suffix('').parts)
        modules[mod] = rel
        if mod.endswith('.__init__'):
            modules[mod[:-9]] = rel
    files = {}
    for p in paths:
        rel = p.relative_to(root).as_posix()
        source = p.read_text(encoding='utf-8', errors='replace')
        try:
            tree = ast.parse(source, filename=rel)
        except SyntaxError:
            files[rel] = {'symbols': [], 'imports': [], 'neighbors': [], 'syntax_error': True}
            continue
        symbols = [n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0:
                    base = node.module or ''
                else:
                    current = list(p.relative_to(root).with_suffix('').parts)
                    package = current if p.name == '__init__.py' else current[:-1]
                    base = '.'.join(package[:max(0, len(package) - node.level + 1)] + ([node.module] if node.module else []))
                imports.append(base)
                imports.extend(f'{base}.{alias.name}' for alias in node.names if base)
        neighbors = set()
        for imp in imports:
            parts = imp.split('.')
            for length in range(len(parts), 0, -1):
                target = modules.get('.'.join(parts[:length]))
                if target and target != rel:
                    neighbors.add(target)
                    break
        files[rel] = {'symbols': symbols, 'imports': imports, 'neighbors': sorted(neighbors), 'syntax_error': False}
    # Treat import relationships as traversable in both directions for context expansion.
    for src, info in list(files.items()):
        for dst in info['neighbors']:
            files[dst]['neighbors'] = sorted(set(files[dst]['neighbors']) | {src})
    return {'root': str(root), 'files': files}


def search(index: dict, query: str, limit: int = 5, graph_weight: float = 0.35) -> list[dict]:
    if limit < 1:
        raise ValueError('limit must be positive')
    q = tokens(query)
    files = index['files']
    base = {}
    for name, meta in files.items():
        path_terms = tokens(name.replace('/', ' '))
        symbol_terms = set().union(*(tokens(s) for s in meta['symbols'])) if meta['symbols'] else set()
        import_terms = set().union(*(tokens(s) for s in meta['imports'])) if meta['imports'] else set()
        base[name] = 3 * len(q & path_terms) + 2 * len(q & symbol_terms) + 0.5 * len(q & import_terms)
    results = []
    for name, meta in files.items():
        # One-hop graph propagation is deliberately modest; a direct match should dominate.
        neighbor_signal = max((base[n] for n in meta['neighbors']), default=0)
        score = base[name] + graph_weight * neighbor_signal
        if score > 0:
            results.append({'file': name, 'score': round(score, 3), 'direct_score': round(base[name], 3), 'related_files': meta['neighbors']})
    return sorted(results, key=lambda x: (-x['score'], x['file']))[:limit]


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description='Index a Python repository and find related files')
    parser.add_argument('repository', help='Path to a local Python repository')
    parser.add_argument('query', help='Natural-language developer question')
    parser.add_argument('--limit', type=int, default=5)
    parser.add_argument('--baseline', action='store_true', help='Disable graph propagation')
    parser.add_argument('--explain', action='store_true', help='Generate an AI explanation of search results')
    args = parser.parse_args()
    
    index = build_index(args.repository)
    results = search(index, args.query, args.limit, 0 if args.baseline else 0.35)

    output = {
        'indexed_files': len(index['files']),
        'results': results
    }

    if args.explain:
        from .agent import explain
        output['explanation'] = explain(index, args.query, limit=args.limit)

    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()
