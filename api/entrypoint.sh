#!/bin/bash

# Upgrade database to the newest version.
alembic upgrade head

# Run the API.
uvicorn src.main:app --workers 1 --host 0.0.0.0 --port 8000
