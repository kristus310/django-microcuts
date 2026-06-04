PYTHON_VERSION ?= {{ cookiecutter.python_version }}
PROJECT_SLUG   := {{ cookiecutter.project_slug }}
MANAGE         := uv run manage.py

.DEFAULT_GOAL := help

.PHONY: help install run tailwind-watch migrate migrations shell build collectstatic clean serve test {% if cookiecutter.use_celery == 'yes' %}worker{% endif %}

help:
	@echo "Available commands:"
	@echo "  make install        - Setup python, install deps, and tailwind"
	@echo "  make run            - Start dev server"
	@echo "  make tailwind-watch - Watch tailwind changes"
	@echo "  make migrate        - Run migrations"
	@echo "  make migrations     - Create migrations"
	@echo "  make superuser      - Create a super user (admin)"
	@echo "  make shell          - Open Django shell"
	@echo "  make build          - Production build (tailwind + static)"
	@echo "  make clean          - Remove pycache and temporary files"
	@echo "  make serve          - Run production gunicorn server"
	@echo "  make test           - Run tests"
{% if cookiecutter.use_celery == 'yes' %}	@echo "  make worker         - Start celery worker"{% endif %}

install:
	mise use python@$(PYTHON_VERSION)
	uv sync --python $$(mise which python)
	$(MANAGE) tailwind setup

run:
	$(MANAGE) tailwind runserver

tailwind-watch:
	$(MANAGE) tailwind watch

shell:
	$(MANAGE) shell

migrate:
	$(MANAGE) migrate

migrations:
	$(MANAGE) makemigrations

superuser:
	$(MANAGE) createsuperuser

build:
	$(MANAGE) tailwind build
	$(MANAGE) collectstatic --no-input

collectstatic:
	$(MANAGE) collectstatic --no-input

serve:
	uv run gunicorn core.wsgi:application --bind 0.0.0.0:8000
{% if cookiecutter.use_celery == 'yes' -%}
worker:
	uv run celery -A core worker -l info
{%- endif %}
test:
	$(MANAGE) test

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -exec rm -f {} +