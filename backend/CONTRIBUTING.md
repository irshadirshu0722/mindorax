# Contributing Guide

Thanks for contributing to Mindorax Backend.

## Before You Start

- Read [`README.md`](README.md) for setup and repository conventions.
- Review the project docs in [`docs/README.md`](docs/README.md).
- Check [`docs/known_issues.md`](docs/known_issues.md) before opening bug-fix PRs so you do not duplicate planned work.

## Development Workflow

1. Create a branch from the latest default branch.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run the local dependencies or start the Docker stack.
4. Make focused changes with clear commit history.
5. Run `python manage.py check`.
6. Run tests relevant to your change.
7. Update docs when behavior, API contracts, or setup steps change.

## Branch Naming

Use descriptive branch names such as:

- `feature/quiz-history-ui-support`
- `fix/refresh-cookie-flow`
- `docs/api-reference-refresh`

## Pull Request Checklist

- The change is scoped to a single concern.
- Documentation is updated when behavior changes.
- New environment or runtime assumptions are documented.
- Commands in `Makefile` and deployment files still make sense.
- No secrets, personal data, or uploaded files were added accidentally.

## Coding Expectations

- Preserve the current layered structure: controller -> service -> repository.
- Keep business rules in services, not controllers.
- Keep docs honest about current behavior, even when that behavior is imperfect.
- Prefer small, reviewable pull requests over broad refactors.

## Reporting Bugs

Include:

- What you expected to happen
- What actually happened
- Reproduction steps
- API route or module affected
- Logs, stack trace, or screenshots when available

## Security Reports

Please do not open public issues for security-sensitive findings. Follow the process in [`SECURITY.md`](SECURITY.md).
