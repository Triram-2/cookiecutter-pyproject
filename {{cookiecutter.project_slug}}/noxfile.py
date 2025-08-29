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
    """Устанавливает проект и его зависимости из указанных групп используя uv pip install."""
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
    """Запускает линтеры (Ruff, Pyright) и проверку формата."""
    session.log("Установка зависимостей для линтинга...")
    install_project_with_deps(session, "lint")

    session.log("Запуск Ruff (format)...")
    session.run("ruff", "format", ".")

    session.log("Запуск Ruff (check)...")
    session.run("ruff", "check", ".", "--fix")

    session.log("Запуск Pyright...")
    session.run("pyright", ".")

    session.log("Линтинг завершен успешно.")


@nox.session(python=PYTHON_VERSIONS)
def test(session: Session) -> None:
    """Запускает тесты с pytest, coverage и hypothesis"""
    session.log("Установка зависимостей для тестирования...")
    install_project_with_deps(session, "test")

    session.log("Запуск тестов с coverage...")
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

    session.log(f"Проверка покрытия кода (должно быть >= {COVERAGE_FAIL_UNDER}%)...")
    session.run("coverage", "report", "-m", f"--fail-under={COVERAGE_FAIL_UNDER}")

    session.log("Генерация отчета о покрытии в формате HTML и XML...")
    session.run("coverage", "html", "-d", "tests/report/coverage")
    session.run("coverage", "xml", "-o", "tests/report/coverage.xml")

    session.log("Тестирование завершено успешно.")


@nox.session(python=None)
def audit(session: Session) -> None:
    """Запускает аудит зависимостей с `pip-audit`"""
    session.log("Установка зависимостей для аудита...")

    create_dev_data_dir()

    session.log("Запуск pip-audit для проверки уязвимостей...")
    session.run("pip-audit", "--local", "-o", "tests/report/pip-audit.txt", ".")

    session.log("Аудит зависимостей завершён.")


@nox.session(python=PYTHON_VERSIONS[0])
def profile(session: Session) -> None:
    """Запуск профилировщика Scalene."""
    session.log("Установка зависимостей для профилирования...")
    install_project_with_deps(session, "profile")

    session.log("Запуск Scalene...")
    try:
        session.run("scalene", f"src/{PROJECT_NAME}/main.py", *session.posargs)

        outfile = PYPROJECT_CONTENT.get("tool", {}).get("scalene", {}).get("outfile")

        session.log(f"Отчет Scalene сохранен в: {Path(outfile).resolve()}")
    except Exception as e:
        session.error(f"Ошибка при запуске Scalene: {e}. Проверьте команду запуска и конфигурацию.")


@nox.session(python=PYTHON_VERSIONS[0])
def locust(session: Session) -> None:
    """Запускает нагрузочное тестирование с Locust."""
    session.log("Установка зависимостей для Locust...")
    install_project_with_deps(session, "loadtest")

    locust_file: str = "locustfile.py"
    if not Path(locust_file).exists():
        session.warn(f"Файл {locust_file} не найден. Для запуска Locust необходимо создать его и определить сценарии нагрузки.")
        session.log(
            "Пример команды, если locustfile.py существует: "
            "locust -f locustfile.py --host=http://localhost:{{cookiecutter.app_port_host}}"
        )
        return

    session.log(f"Запуск Locust (используя {locust_file})...")
    session.run("locust", "-f", locust_file, *session.posargs)


@nox.session(python=False)
def clean(session: Session) -> None:
    """Удаляет временные файлы и папки сборки/тестирования."""
    session.log("Очистка...")
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
                session.log(f"Удаление {path_obj}")
                if path_obj.is_dir():
                    shutil.rmtree(path_obj, ignore_errors=True)
                else:
                    path_obj.unlink(missing_ok=True)
    session.log("Очистка завершена.")


@nox.session(python=False)
def _commit(session: Session) -> None:  # type: ignore[reportUnusedFunction]
    """Добавление проекта в git и коммит через commitizen"""
    session.run("git", "add", ".")
    session.run("cz", "commit")


@nox.session
def commit(session: Session) -> None:
    """Полный CI-цикл и коммит лишь при отсутствии ошибок"""
    session.run("nox", "-s", "ci-3.13", external=True)
    session.run("nox", "-s", "clean", external=True)
    session.run("nox", "-s", "_commit", external=True)


@nox.session(python=False)
def bump(session: Session) -> None:
    """Bump через commitizen + `git push -u origin main`"""
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
    session.log(f"Запуск CI для Python {python_version}")

    suffix = f"-{python_version}" if isinstance(python_version, str) else ""
    session.notify(f"lint{suffix}")
    session.notify(f"test{suffix}")
