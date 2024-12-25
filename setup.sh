#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Default hostname
hostname=${1:-localhost}

# Log message function
log_message() {
    echo "=== $1 ==="
}

log_message "Cloning DocrepoX repository"
if git clone https://github.com/documendous/docrepox.git; then
    log_message "Repository cloned successfully"
else
    echo "Error: Failed to clone repository. Exiting."
    exit 1
fi

log_message "Navigating to DocrepoX directory"
if cd docrepox; then
    log_message "In DocrepoX directory"
else
    echo "Error: Failed to enter docrepox directory. Exiting."
    exit 1
fi

log_message "Processing hostname for DJANGO_ALLOWED_HOSTS"
if grep -q "DJANGO_ALLOWED_HOSTS" env.prod.example; then
    if ! grep -q "DJANGO_ALLOWED_HOSTS=.*$hostname" env.prod.example; then
        sed -i "s/^DJANGO_ALLOWED_HOSTS=.*/&,$hostname/" env.prod.example
        log_message "Added $hostname to DJANGO_ALLOWED_HOSTS"
    else
        log_message "$hostname is already in DJANGO_ALLOWED_HOSTS. No changes made"
    fi
else
    echo "DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1],$hostname" >> env.prod.example
    log_message "Created DJANGO_ALLOWED_HOSTS with $hostname"
fi

log_message "Setting up Python environment"
python -m venv .venv
. .venv/bin/activate
log_message "Python environment set up successfully"

log_message "Installing dependencies"
pip install poetry
poetry export --with dev -f requirements.txt --output requirements.txt
cp requirements.txt docrepo/requirements.txt
mkdir -p docrepo/mediafiles
cp env.prod.example .env.prod
cp env.prod.db.example .env.prod.db
cp .env.prod docrepo/.env.prod
log_message "Dependencies installed successfully"

log_message "Applying database migrations"
python manage.py makemigrations
python manage.py migrate
log_message "Database migrated successfully"

log_message "Collecting static files"
python manage.py collectstatic --noinput
log_message "Static files collected successfully"

log_message "Starting DocrepoX with Docker"
docker compose -f docker-compose.prod.yml up --build
