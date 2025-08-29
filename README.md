# Cookiecutter PyProject

[![----------------------](https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/misc/transparent.png)](#)
<p align="center">
    <img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/logos/exports/1544x1544_circle.png" />
</p>
<h1 align="center">Cookiecutter template for Python project</h1>
<p align="center">
    <a href="https://github.com/Triram-2/cookiecutter-pyproject/stargazers">
        <img alt="Stargazers" src="https://img.shields.io/github/stars/Triram-2/cookiecutter-pyproject?style=for-the-badge&logo=starship&color=C9CBFF&logoColor=D9E0EE&labelColor=302D41"></a>
    <a href="https://github.com/Triram-2/cookiecutter-pyproject/issues">
        <img alt="Issues" src="https://img.shields.io/github/issues/Triram-2/cookiecutter-pyproject?style=for-the-badge&logo=gitbook&color=F2CDCD&logoColor=D9E0EE&labelColor=302D41"></a>
    <a href="https://github.com/Triram-2/cookiecutter-pyproject/blob/main/LICENSE">
        <img alt="License" src="https://img.shields.io/github/license/Triram-2/cookiecutter-pyproject?style=for-the-badge&logo=github&color=B5E8E0&logoColor=D9E0EE&labelColor=302D41"></a>
</p>

Шаблон [Cookiecutter](https://github.com/cookiecutter/cookiecutter) для создания современных проектов на Python.

Этот шаблон создает основу проекта с настроенными инструментами для линтинга, форматирования, тестирования, автоматизации задач и управления зависимостями, позволяя вам сосредоточиться на написании кода.

## Особенности

- **Управление зависимостями**: Использует `pyproject.toml` и [UV](https://github.com/astral-sh/uv) для быстрого и надежного управления зависимостями.
- **Автоматизация задач**: [Nox](https://nox.thea.codes/) для автоматизации линтинга, тестов, аудита и других задач.
- **Линтинг и форматирование**: Настроенный [Ruff](https://github.com/astral-sh/ruff) для сверхбыстрого линтинга и форматирования кода.
- **Проверка типов**: Статическая проверка типов с помощью [Pyright](https://github.com/microsoft/pyright).
- **Тестирование**: Готовая структура для тестов с использованием [Pytest](https://pytest.org/), включая отчеты о покрытии ([Coverage.py](https://coverage.readthedocs.io/)) и property-based тестирование ([Hypothesis](https://hypothesis.readthedocs.io/)).
- **Стандартизация коммитов**: Интеграция с [Commitizen](https://commitizen-tools.github.io/commitizen/) для стандартизированных сообщений коммитов (Conventional Commits).
- **Аудит безопасности**: Проверка уязвимостей в зависимостях с помощью [pip-audit](https://pypi.org/project/pip-audit/).
- **Профилирование**: Встроенная задача для профилирования кода с помощью [Scalene](https://github.com/plasma-umass/scalene).
- **Контейнеризация (опционально)**: Возможность включения `Dockerfile` и `docker-compose` для различных окружений.
- **CI/CD (опционально)**: Базовый шаблон для `.gitlab-ci.yml`.
- **Гибкость**: Множество опций для включения/отключения функциональности в зависимости от нужд проекта.

## Требования

Убедитесь, что у вас установлен `cookiecutter`:
```bash
pipx install cookiecutter
```

## Использование

Чтобы создать новый проект, выполните команду:

```bash
cookiecutter gh:Triram-2/cookiecutter-pyproject
```

Вам будет предложено ввести следующие параметры:

| Параметр | Описание                                                              | Значение по умолчанию                 |
|---|-----------------------------------------------------------------------|---------------------------------------|
| `project_name` | Название проекта.                                                     | `My Amazing Project`                  |
| `project_slug` | Имя каталога проекта (генерируется из `project_name`).                | `my_amazing_project`                  |
| `author_name` | Ваше имя.                                                             | `Your Name`                           |
| `author_email` | Ваш email.                                                            | `your.email@example.com`              |
| `year` | Текущий год.                                                          | `2025`                                |
| `version` | Начальная версия проекта.                                             | `0.0.0`                               |
| `description` | Краткое описание проекта.                                             | `A short description...`              |
| `python_version` | Выбор версии Python.                                                  | `3.12` / `3.13` / `3.14`              |
| `use_configs` | Использовать ли полноценную папку configs с разделением по окружениям | `y` / `n`                             |
| `use_dot_env` | Использовать ли `.env` файл для переменных окружения.                 | `y` / `n`                             |
| `use_docker` | Включить ли файлы для Docker.                                         | `y` / `n`                             |
| `use_k8s` | Включить ли каталог для Kubernetes.                                   | `y` / `n`                             |
| `use_gitlab` | Включить ли `.gitlab-ci.yml` и .gitlab                                | `y` / `n`                             |
| `use_todo_md` | Создать ли файл `TODO.md`.                                            | `y` / `n`                             |
| `license` | Выбор лицензии.                                                       | `MIT`, `BSD`, `Apache`, `GPL`, `none` |

## Структура сгенерированного проекта

После генерации вы получите следующую структуру каталогов:

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

## Работа с сгенерированным проектом

Все основные команды для разработки, тестирования и сборки управляются через `nox`.

### Установка

Для начала установите `nox` и `uv` (рекомендуется):
```bash
pipx install nox uv
```

### Доступные команды

Выполните `nox -l`, чтобы увидеть список всех доступных сессий.

- **`nox -s lint`**: Запускает проверку кода с помощью Ruff и Pyright.
- **`nox -s test`**: Запускает тесты с помощью Pytest и выводит отчет о покрытии(Coverage).
- **`nox -s audit`**: Проверяет зависимости на наличие уязвимостей.
- **`nox -s profile`**: Запускает профилирование кода.
- **`nox -s ci`**: Выполняет полный цикл CI (линтинг + тесты).
- **`nox -s commit`**: Запускает `cz commit` после успешного прохождения CI.
- **`nox -s bump`**: Обновляет версию проекта с помощью `cz bump` и отправляет изменения.
- **`nox -s release`**: Комбинирует `commit` и `bump` для создания релиза.
- **`nox -s clean`**: Удаляет временные файлы и кэш.

## Лицензия

Этот шаблон распространяется под лицензией [MIT](./LICENSE). Сгенерированный проект будет иметь лицензию, выбранную вами при создании.
