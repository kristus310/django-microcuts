PYTHON_VERSION ?= {{ cookiecutter.python_version }}
PROJECT_SLUG   := {{ cookiecutter.project_slug }}
MANAGE         := uv run manage.py

BLUE  := \033[36m
RESET := \033[0m

.DEFAULT_GOAL := help

.PHONY: help install run tailwind-watch migrate migrations shell build collectstatic clean serve {% if cookiecutter.use_celery == 'yes' %}worker{% endif %}

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(BLUE)%-20s$(RESET) %s\n", $$1, $$2}'

install:
	mise use python@$(PYTHON_VERSION)
	uv sync
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

build:
	$(MANAGE) tailwind build
	$(MANAGE) collectstatic --no-input

collectstatic:
	$(MANAGE) collectstatic --no-input

serve:
	uv run gunicorn $(PROJECT_SLUG).wsgi:application --bind 0.0.0.0:8000
{% if cookiecutter.use_celery == 'yes' -%}
worker:
	uv run celery -A $(PROJECT_SLUG) worker -l info
{%- endif %}
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -exec rm -f {} +