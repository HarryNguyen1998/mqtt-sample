#!/bin/bash

# Upgrade database to the newest version.
alembic upgrade head

# Run the API.
exec uvicorn api.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
