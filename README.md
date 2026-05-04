# django-microcuts

A lightweight [Cookiecutter](https://cookiecutter.readthedocs.io/) template for Django projects. Designed to work with [VS Code](https://code.visualstudio.com/), [mise](https://mise.jdx.dev/), and [uv](https://docs.astral.sh/uv/).

---

## Requirements

- [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/installation.html)
- [mise](https://mise.jdx.dev/)
- [uv](https://docs.astral.sh/uv/)
- [VS Code](https://code.visualstudio.com/)

---

## Usage

```bash
cookiecutter gh:kristus310/django-microcuts
```

You will be prompted to configure your project with the following options:

| Option | Default | Choices |
|---|---|---|
| `project_name` | `Django Project` | any string |
| `author` | `Anonymous` | any string |
| `description` | `A django project.` | any string |
| `language_code` | `en-us` | `en-us`, `cs` |
| `time_zone` | `UTC` | `UTC`, `Europe/Prague` |
| `python_version` | `3.12` | `3.12`, `3.13`, `3.14` |
| `database_type` | `sqlite` | `sqlite`, `postgres` |
| `use_allauth` | `no` | `no`, `yes` |
| `use_pillow` | `no` | `no`, `yes` |
| `use_celery` | `no` | `no`, `yes` |
| `use_htmx` | `no` | `no`, `yes` |

---

## What's included

- Django project scaffold with settings split for dev/prod
- `pyproject.toml` managed by **uv**
- `.mise.toml` for Python version management
- `.vscode/` with recommended extensions and settings
- Optional integrations: `django-allauth`, `Pillow`, `Celery`, `htmx`
- PostgreSQL or SQLite database configuration

---

## License

MIT