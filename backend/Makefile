PYTHON ?= python
MANAGE = $(PYTHON) manage.py
CELERY = $(PYTHON) -m celery -A core

.PHONY: help install migrate makemigrations check test run worker shell createsuperuser compose-up compose-down compose-logs

help:
	@echo "Available targets:"
	@echo "  install         Install Python dependencies"
	@echo "  migrate         Run Django migrations"
	@echo "  makemigrations  Create Django migrations"
	@echo "  check           Run Django system checks"
	@echo "  test            Run Django tests"
	@echo "  run             Start the Django development server"
	@echo "  worker          Start the Celery worker"
	@echo "  shell           Open the Django shell"
	@echo "  createsuperuser Create a Django superuser"
	@echo "  compose-up      Build and start the Docker stack"
	@echo "  compose-down    Stop the Docker stack"
	@echo "  compose-logs    Follow Docker compose logs"

install:
	$(PYTHON) -m pip install -r requirements.txt

migrate:
	$(MANAGE) migrate

makemigrations:
	$(MANAGE) makemigrations

check:
	$(MANAGE) check

test:
	$(MANAGE) test

run:
	$(MANAGE) runserver

worker:
	$(CELERY) worker -l info

shell:
	$(MANAGE) shell

createsuperuser:
	$(MANAGE) createsuperuser

compose-up:
	docker compose up --build

compose-down:
	docker compose down

compose-logs:
	docker compose logs -f
