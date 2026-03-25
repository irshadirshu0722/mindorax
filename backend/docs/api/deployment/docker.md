# Docker Deployment Guide

## Goal

The repository now includes a Docker image and compose stack for running:

- Django API
- Celery worker
- PostgreSQL
- Redis

without changing `apps/` or `core/`.

## Why The Compose File Looks Unusual

The current Django settings hard-code:

- PostgreSQL at `localhost:5432`
- Redis at `localhost:6379`

In a typical compose deployment, the app would connect to service names such as `db` and `redis`. Because the code was intentionally left untouched, the compose stack uses a shared network namespace pattern so all runtime services can still talk to each other through `127.0.0.1`.

## Services

### `runtime`

- lightweight namespace holder
- publishes port `8000`

### `db`

- PostgreSQL 16
- persists data in `postgres_data`

### `redis`

- Redis 7
- persists data in `redis_data`

### `app`

- builds from the project `Dockerfile`
- waits for PostgreSQL and Redis
- runs migrations on startup
- serves Django through Gunicorn on port `8000`

### `worker`

- builds from the same image
- waits for PostgreSQL and Redis
- runs the Celery worker

## Start The Stack

```bash
docker compose up --build
```

Run in detached mode:

```bash
docker compose up --build -d
```

Stop the stack:

```bash
docker compose down
```

## Published Port

By default the API is exposed on:

- `http://localhost:8000`

You can override the published port:

```bash
APP_PORT=8080 docker compose up --build
```

## Volumes

- `postgres_data` for PostgreSQL data
- `redis_data` for Redis persistence
- `media_data` for uploaded files used by both the app and Celery worker

## Health Checks

The compose file includes health checks for:

- PostgreSQL
- Redis
- Django API

## Production Caveats

This setup is intentionally compatible with the current source code, but it is not the final ideal production architecture.

Recommended future improvements:

1. move all settings to environment variables
2. let Django connect to named services instead of `localhost`
3. add a reverse proxy such as Nginx or Traefik
4. configure static file handling explicitly
5. replace hard-coded secrets before any public deployment
