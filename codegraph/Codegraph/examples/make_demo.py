"""Demonstrate CodeGraph using a small sample project."""

from pathlib import Path
import tempfile

from codegraph.Codegraph.core import build_index, search

with tempfile.TemporaryDirectory() as folder:
    root = Path(folder)

    (root / "login.py").write_text(
        "def authenticate(user, password):\n"
        "    return check_password(password)\n"
    )

    (root / "validators.py").write_text(
        "def check_password(password):\n"
        "    return len(password) > 8\n"
    )

    (root / "billing.py").write_text(
        "def create_invoice(amount):\n"
        "    return amount\n"
    )

    index = build_index(root)

    for item in search(index, "login authenticate password"):
        print(item)
        