import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent / "{{ cookiecutter.project_slug }}"
sys.path.insert(0, str(root))


__all__ = ['__version__']

__version__ = "{{ cookiecutter.version }}"