#!/bin/sh
set -eu

python /app/docker/wait_for_services.py

exec python -m celery -A core worker \
  -l "${CELERY_LOGLEVEL:-info}" \
  --concurrency="${CELERY_CONCURRENCY:-2}"
