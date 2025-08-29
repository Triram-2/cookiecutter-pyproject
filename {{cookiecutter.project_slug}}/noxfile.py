import os
import shutil
import tomllib

from pathlib import Path
from typing import Any, Dict, List, Iterator

import nox

from nox import Session


nox.options.default_venv_backend = "uv"

PYPROJECT_CONTENT: Dict[str, Any] = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

PROJECT_NAME: str = PYPROJECT_CONTENT["project"]["name"]
PYTHON_VERSIONS: List[str] = ["3.12", "3.13"]
SRC_DIR: str = "src"
TESTS_DIR: str = "tests"
DOCS_DIR: str = "docs"
COVERAGE_FAIL_UNDER: int = 50  # TODO: change to 80-99
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"


def install_project_with_deps(session: Session, *groups: str) -> None:
    """Installs the project and its dependencies from the specified groups using uv pip install."""
    install_args: List[str] = ["-e", f".[{','.join(groups)}]"] if groups else ["-e", "."]
    # Construct a string for logging that represents the command as it would be typed
    log_command_str = "uv pip install " + " ".join(install_args)
    session.log(f"Installing with: {log_command_str}")
    session.run_always("uv", "pip", "install", *install_args, external=True)
    session.log(f"Finished: {log_command_str}")


def create_dev_data_dir():
    current_dir = os.path.dirname(__file__)
    dev_dir = os.path.join(current_dir, "tests", "report", "coverage")
    os.makedirs(dev_dir, mode=775, exist_ok=True)


@nox.session(python=PYTHON_VERSIONS)
def lint(session: Session) -> None:
    """Runs linters (Ruff, Pyright) and format check."""
    session.log("Installing dependencies for linting...")
    install_project_with_deps(session, "lint")

    session.log("Running Ruff (format)...")
    session.run("ruff", "format", ".")

    session.log("Running Ruff (check)...")
    session.run("ruff", "check", ".", "--fix")

    session.log("Running Pyright...")
    session.run("pyright", ".")

    session.log("Linting finished successfully.")


@nox.session(python=PYTHON_VERSIONS)
def test(session: Session) -> None:
    """Runs tests with pytest, coverage and hypothesis"""
    session.log("Installing dependencies for testing...")
    install_project_with_deps(session, "test")

    session.log("Running tests with coverage...")
    session.run(
        "coverage",
        "run",
        "--source",
        SRC_DIR,
        "-m",
        "pytest",
        TESTS_DIR,
        *session.posargs,
        env={
            "PYTHONPATH": SRC_DIR,
            "ENVIRONMENT": "DEVELOPMENT",
            "VAULT_ADDR": "http://localhost:8200",
            "VAULT_TOKEN": "test_token",
        },
    )

    session.log(f"Checking code coverage (should be >= {COVERAGE_FAIL_UNDER}%)...")
    session.run("coverage", "report", "-m", f"--fail-under={COVERAGE_FAIL_UNDER}")

    session.log("Generating coverage report in HTML and XML format...")
    session.run("coverage", "html", "-d", "tests/report/coverage")
    session.run("coverage", "xml", "-o", "tests/report/coverage.xml")

    session.log("Testing finished successfully.")


@nox.session(python=None)
def audit(session: Session) -> None:
    """Runs dependency audit with `pip-audit`"""
    session.log("Installing dependencies for auditing...")

    create_dev_data_dir()

    session.log("Running pip-audit to check for vulnerabilities...")
    session.run("pip-audit", "--local", "-o", "tests/report/pip-audit.txt", ".")

    session.log("Dependency audit finished.")


@nox.session(python=PYTHON_VERSIONS[0])
def profile(session: Session) -> None:
    """Runs the Scalene profiler."""
    session.log("Installing dependencies for profiling...")
    install_project_with_deps(session, "profile")

    session.log("Running Scalene...")
    try:
        session.run("scalene", f"src/{PROJECT_NAME}/main.py", *session.posargs)

        outfile = PYPROJECT_CONTENT.get("tool", {}).get("scalene", {}).get("outfile")

        session.log(f"Scalene report saved to: {Path(outfile).resolve()}")
    except Exception as e:
        session.error(f"Error running Scalene: {e}. Check the launch command and configuration.")


@nox.session(python=PYTHON_VERSIONS[0])
def locust(session: Session) -> None:
    """Runs load testing with Locust."""
    session.log("Installing dependencies for Locust...")
    install_project_with_deps(session, "loadtest")

    locust_file: str = "locustfile.py"
    if not Path(locust_file).exists():
        session.warn(f"File {locust_file} not found. To run Locust, you need to create it and define load scenarios.")
        session.log(
            "Example command if locustfile.py exists: "
            "locust -f locustfile.py --host=http://localhost:8000"
        )
        return

    session.log(f"Running Locust (using {locust_file})...")
    session.run("locust", "-f", locust_file, *session.posargs)


@nox.session(python=False)
def clean(session: Session) -> None:
    """Removes temporary build/test files and folders."""
    session.log("Cleaning...")
    patterns_to_remove: List[str] = [
        "**/dist/**",
        "**/build",
        "**/*.egg-info",
        "**/.pytest_cache",
        "**/.ruff_cache",
        "**/scalene*.html",
        "**/__pycache__",
        "**/_build",
        "**/pip-audit.txt.coverage",
        "**/.coverage*",
        "**/tests/report/**",
        "**/logs",
    ]
    for pattern in patterns_to_remove:
        if "*" in pattern or "?" in pattern:
            path_iter: Iterator[Path] = Path(".").glob(pattern)
            for path_obj in path_iter:
                session.log(f"Removing {path_obj}")
                if path_obj.is_dir():
                    shutil.rmtree(path_obj, ignore_errors=True)
                else:
                    path_obj.unlink(missing_ok=True)
    session.log("Cleaning finished.")


@nox.session(python=False)
def _commit(session: Session) -> None:  # type: ignore[reportUnusedFunction]
    """Adds the project to git and commits via commitizen"""
    session.run("git", "add", ".")
    session.run("cz", "commit")


@nox.session
def commit(session: Session) -> None:
    """Full CI cycle and commit only if there are no errors"""
    session.run("nox", "-s", "ci-3.13", external=True)
    session.run("nox", "-s", "clean", external=True)
    session.run("nox", "-s", "commit", external=True)


@nox.session(python=False)
def bump(session: Session) -> None:
    """Bump via commitizen + `git push -u origin main`"""
    session.run("cz", "bump")
    session.run("git", "push", "-u", "origin", "develop")


@nox.session(python=False)
def release(session: Session) -> None:
    """commit+bump"""
    session.notify("commit")
    session.notify("bump")


@nox.session(python=PYTHON_VERSIONS, name="ci")
def ci_pipeline(session: nox.Session) -> None:
    """lint+test"""
    python_version = session.python
    session.log(f"Running CI for Python {python_version}")

    suffix = f"-{python_version}" if isinstance(python_version, str) else ""
    session.notify(f"lint{suffix}")
    session.notify(f"test{suffix}")