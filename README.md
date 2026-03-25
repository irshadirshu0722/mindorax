# Mindorax Backend

Mindorax Backend is a Django 6 + Django Ninja API for an AI-assisted study planner. It supports Google-based sign-in, subject management, file uploads, AI subject analysis, AI-generated study plans, quizzes, and quiz attempt tracking.

## What The Project Currently Includes

- Django 6 project with modular apps for `users`, `subjects`, `planning`, `quizzes`, and `logs`
- Django Ninja API mounted at `/api/`
- PostgreSQL as the primary database
- Redis as cache and Celery broker
- Celery background jobs for subject analysis, study plan generation, and quiz generation
- Google OAuth token verification
- Gemini-powered study analysis, planning, and quiz generation

## Quick Start

### Local development

1. Create and activate a Python 3.13 virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Make sure PostgreSQL is available on `localhost:5432` with:
   - database: `studyplanner`
   - username: `postgres`
   - password: `irshad1213`
4. Make sure Redis is available on `localhost:6379`.
5. Run `python manage.py migrate`.
6. Start the API with `python manage.py runserver`.
7. Start the Celery worker with `python -m celery -A core worker -l info`.

### Docker deployment

Run:

```bash
docker compose up --build
```

The provided `docker-compose.yml` is designed to work with the current codebase without editing `apps/` or `core/`. Because Django settings currently hard-code PostgreSQL and Redis on `localhost`, the compose stack uses a shared network namespace workaround so the app, worker, PostgreSQL, and Redis can still communicate correctly.

## API Docs

- Swagger UI: `/api/docs`
- OpenAPI JSON: `/api/openapi.json`
- Detailed written API reference: [`docs/api/reference.md`](docs/api/reference.md)
- Frontend integration guide: [`docs/frontend-integration.md`](docs/frontend-integration.md)

## Documentation Map

- Docs index: [`docs/README.md`](docs/README.md)
- Architecture: [`docs/architecture.md`](docs/architecture.md)
- Project analysis: [`docs/project_analysis.md`](docs/project_analysis.md)
- Database structure: [`docs/database_structure.md`](docs/database_structure.md)
- Authentication: [`docs/features/authentication.md`](docs/features/authentication.md)
- API reference: [`docs/api/reference.md`](docs/api/reference.md)
- Docker deployment: [`docs/deployment/docker.md`](docs/deployment/docker.md)
- Known issues and constraints: [`docs/known_issues.md`](docs/known_issues.md)
- Delivery roadmap: [`docs/project_plan.md`](docs/project_plan.md)

## Important Current Constraints

- The project currently stores multiple secrets and connection settings directly in `core/settings.py`.
- Login returns JWTs in the response body, but authenticated endpoints read the access token from cookies.
- Subject creation responses do not expose the subject `id`.
- Create-plan and create-quiz endpoints are asynchronous and return only confirmation messages, not created resource IDs.
- The current Gemini SDK import emits a deprecation warning during `manage.py check`.

## Open Source Project Files

This repository now includes:

- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `Makefile`
- `Dockerfile`
- `docker-compose.yml`
- `.gitignore`
- `.dockerignore`

## Verification

The repository imports successfully with:

```bash
python manage.py check
```

That check also reports the current deprecation warning for `google.generativeai`, which is documented in [`docs/known_issues.md`](docs/known_issues.md).
