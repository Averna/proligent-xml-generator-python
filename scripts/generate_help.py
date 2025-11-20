"""
Generate simple HTML help files from the library docstrings.

The script renders documentation for selected public modules using Python's
standard ``pydoc`` generator and writes the output to ``build/help``.
"""

from importlib import import_module
from pathlib import Path
import pydoc
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "build" / "help"
MODULES = {
    "proligent.model": "proligent-model.html",
    "proligent.xml_validate": "proligent-xml-validate.html",
}


def main() -> None:
    # Ensure the source tree is on sys.path so modules import without install.
    sys.path.insert(0, str(ROOT / "src"))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc_builder = pydoc.HTMLDoc()

    for module_name, filename in MODULES.items():
        module = import_module(module_name)
        html = doc_builder.document(module)
        (OUT_DIR / filename).write_text(html, encoding="utf-8")

    print(f"Generated help docs in: {OUT_DIR}")  # noqa: T201


if __name__ == "__main__":
    main()
