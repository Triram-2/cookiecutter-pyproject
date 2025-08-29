import sys
from pathlib import Path

root: Path = Path(__file__).resolve().parent.parent / "src" / "{{ cookiecutter.project_slug }}"
root_tests: Path = Path(__file__).resolve().parent

sys.path.insert(0, str(root))
sys.path.insert(0, str(root_tests))