<h1 align="center">Cookiecutter template for Python project</h1>
<p align="center">
    <a href="https://github.com/Triram-2/cookiecutter-pyproject/stargazers">
        <img alt="Stargazers" src="https://img.shields.io/github/stars/Triram-2/cookiecutter-pyproject?style=for-the-badge&logo=starship&color=C9CBFF&logoColor=D9E0EE&labelColor=302D41"></a>
    <a href="https://github.com/Triram-2/cookiecutter-pyproject/issues">
        <img alt="Issues" src="https://img.shields.io/github/issues/Triram-2/cookiecutter-pyproject?style=for-the-badge&logo=gitbook&color=F2CDCD&logoColor=D9E0EE&labelColor=302D41"></a>
    <a href="https://github.com/Triram-2/cookiecutter-pyproject/blob/main/LICENSE">
        <img alt="License" src="https://img.shields.io/github/license/Triram-2/cookiecutter-pyproject?style=for-the-badge&logo=github&color=B5E8E0&logoColor=D9E0EE&labelColor=302D41"></a>
</p>

A [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template designed for other cookiecutter templates (!).
It is not intended for real projects, as it is too generalized.

This template creates a project base with configured tools for linting, formatting, testing, task automation, and dependency management, allowing you to focus on writing code.

## Features

- **Dependency Management**: Uses `pyproject.toml` and [UV](https://github.com/astral-sh/uv) for fast and reliable dependency management.
- **Task Automation**: [Nox](https://nox.thea.codes/) for automating linting, tests, auditing, and other tasks.
- **Linting and Formatting**: Configured [Ruff](https://github.com/astral-sh/ruff) for super-fast linting and code formatting.
- **Type Checking**: Static type checking with [Pyright](https://github.com/microsoft/pyright).
- **Testing**: Ready-made structure for tests using [Pytest](https://pytest.org/), including coverage reports ([Coverage.py](https://coverage.readthedocs.io/)) and property-based testing ([Hypothesis](https://hypothesis.readthedocs.io/)).
- **Commit Standardization**: Integration with [Commitizen](https://commitizen-tools.github.io/commitizen/) for standardized commit messages (Conventional Commits).
- **Security Audit**: Vulnerability checking in dependencies with [pip-audit](https://pypi.org/project/pip-audit/).
- **Profiling**: Built-in task for code profiling with [Scalene](https://github.com/plasma-umass/scalene).
- **Containerization (optional)**: Ability to include `Dockerfile` and `docker-compose` for various environments.
- **CI/CD (optional)**: Basic template for `.gitlab-ci.yml`.
- **Flexibility**: Many options to enable/disable functionality depending on project needs.

## Requirements

Make sure you have `cookiecutter` installed:
```bash
pipx install cookiecutter
```

## Usage

To create a new project, run the command:

```bash
cookiecutter gh:Triram-2/cookiecutter-pyproject
```

You will be prompted to enter the following parameters:

| Parameter | Description                                                              | Default Value                     |
|---|-----------------------------------------------------------------------|-------------------------------------------|
| `project_name` | The name of the project.                                                     | `My Amazing Project`                      |
| `project_slug` | The project directory name (generated from `project_name`).                | `my_amazing_project`                      |
| `author_name` | Your name.                                                             | `Your Name`                               |
| `author_email` | Your email.                                                            | `your.email@example.com`                  |
| `year` | Current year.                                                          | `2025`                                    |
| `version` | Initial project version.                                             | `0.0.0`                                   |
| `description` | A short description of the project.                                             | `A short description...`                  |
| `python_version` | Python version selection.                                                  | `3.12` / `3.13` / `3.14`                  |
| `use_configs` | Whether to use a full configs folder with environment separation | `y` / `n`                                 |
| `use_dot_env` | Whether to use a `.env` file for environment variables.                 | `y` / `n`                                 |
| `use_docker` | Whether to include Docker files.                                         | `y` / `n`                                 |
| `use_k8s` | Whether to include a Kubernetes directory.                                   | `y` / `n`                                 |
| `use_gitlab` | Whether to include `.gitlab-ci.yml` and .gitlab                                | `y` / `n`                                 |
| `use_todo_md` | Whether to create a `TODO.md` file.                                            | `y` / `n`                                 |
| `license` | License selection.                                                       | `MIT` / `BSD` / `Apache` / `GPL` / `none` |

## Generated Project Structure

After generation, you will get the following directory structure:

```
{{cookiecutter.project_slug}}/
├───.env
├───.gitignore
├───.gitlab-ci.yml
├───.python-version
├───CHANGELOG.md
├───noxfile.py
├───pyproject.toml
├───README.md
├───TODO.md
├───configs/
│   ├───common/
│   │   └───.gitkeep
│   ├───demonstration/
│   │   └───system.json
│   ├───development/
│   │   └───system.json
│   ├───production/
│   │   └───system.json
│   ├───staging/
│   │   └───system.json
│   └───testing/
│       └───system.json
├───docker/
│   ├───docker-compose.demo.yml
│   ├───docker-compose.development.yml
│   ├───docker-compose.production.yml
│   ├───docker-compose.staging.yml
│   ├───docker-compose.testing.yml
│   ├───README.md
│   └───images/
│       ├───app/
│       │   └───Dockerfile
│       ├───base/
│       │   ├───base-requirements.txt
│       │   ├───Dockerfile.python
│       │   └───Dockerfile.ubuntu
│       └───database/
│           ├───Dockerfile.MongoDB
│           └───Dockerfile.Redis
├───docs/
│   └───README.md
├───k8s/
│   └───README.md
├───scripts/
│   └───.gitkeep
├───src/
│   └───{{cookiecutter.project_slug}}/
│       └───README.md
└───tests/
    ├───conftest.py
    ├───README.md
    ├───accessibility/
    │   └───.gitkeep
    ├───compatibility/
    │   └───.gitkeep
    ├───e2e/
    │   └───.gitkeep
    ├───fixtures/
    │   ├───__init__.py
    │   ├───clean_modules.py
    │   └───root_of_project.py
    ├───helpers/
    │   └───__init__.py
    ├───integration/
    │   └───.gitkeep
    ├───mocks/
    │   └───__init__.py
    ├───performance/
    │   └───.gitkeep
    ├───security/
    │   └───.gitkeep
    ├───smoke/
    │   └───.gitkeep
    └───unit/
        └───conftest.py
```

## Working with the Generated Project

All main commands for development, testing, and building are managed via `nox`.

### Installation

First, install `nox` and `uv` (recommended):
```bash
pipx install nox uv
```

### Available Commands

Run `nox -l` to see a list of all available sessions.

- **`nox -s lint`**: Runs code checks with Ruff and Pyright.
- **`nox -s test`**: Runs tests with Pytest and outputs a coverage report.
- **`nox -s audit`**: Checks dependencies for vulnerabilities.
- **`nox -s profile`**: Runs code profiling.
- **`nox -l locust`**: Runs Locust load tests.
- **`nox -s ci`**: Executes a full CI cycle (linting + tests).
- **`nox -s commit`**: Runs `cz commit` after successful CI.
- **`nox -s bump`**: Updates the project version with `cz bump` and pushes changes.
- **`nox -s release`**: Combines `commit` and `bump` to create a release.
- **`nox -s clean`**: Removes temporary files and cache.

## License

This template is distributed under the [MIT License](./LICENSE). The generated project will have the license you selected during creation.