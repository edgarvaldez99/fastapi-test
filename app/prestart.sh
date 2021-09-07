#! /usr/bin/env bash

# according to the documentation of the image tiangolo/uvicorn-gunicorn-fastapi
# this script is executed before starting the application.
# For more information:
# https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker#pre_start_path

# Let the DB start
python /app/database/check_is_ready.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python /app/database/initial_data.py
