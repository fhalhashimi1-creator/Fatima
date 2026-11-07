"""Reproducible retrieval evaluation on user-provided labeled tasks."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .core import build_index, search


def evaluate(root: str | Path, tasks: list[dict], k: int = 5) -> dict:
    if not tasks:
        raise ValueError('Evaluation requires at least one labeled task')
    if k < 1:
        raise ValueError('k must be positive')
    index = build_index(root)
    methods = {'lexical': 0.0, 'graph': 0.35}
    report = {'repository': str(Path(root).resolve()), 'indexed_files': len(index['files']), 'tasks': len(tasks), 'k': k, 'methods': {}}
    for name, weight in methods.items():
        records = []
        for task in tasks:
            if not task.get('query') or not task.get('relevant_files'):
                raise ValueError('Each task needs a query and nonempty relevant_files')
            truth = set(task['relevant_files'])
            found = [item['file'] for item in search(index, task['query'], k, weight)]
            records.append({'query': task['query'], 'ground_truth': sorted(truth), 'retrieved': found,
                            'hit_at_k': int(bool(truth.intersection(found))),
                            'recall_at_k': len(truth.intersection(found)) / len(truth)})
        report['methods'][name] = {'hit_at_k': sum(r['hit_at_k'] for r in records) / len(records),
                                   'recall_at_k': sum(r['recall_at_k'] for r in records) / len(records),
                                   'per_task': records}
    return report


def main():
    parser = argparse.ArgumentParser(description='Evaluate graph and lexical retrieval on labeled queries')
    parser.add_argument('repository')
    parser.add_argument('tasks_json', help='JSON array of {query, relevant_files} records')
    parser.add_argument('--k', type=int, default=5)
    parser.add_argument('--output', default='evaluation_results.json')
    args = parser.parse_args()
    report = evaluate(args.repository, json.loads(Path(args.tasks_json).read_text()), args.k)
    Path(args.output).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: {metric: val for metric, val in v.items() if metric != 'per_task'} for k, v in report['methods'].items()}, indent=2))

if __name__ == '__main__':
    main()
