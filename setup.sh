#!/usr/bin/env bash

# Set default hostname if not run interactively
hostname=${1:-localhost}

echo "===Cloning DocrepoX repository==="
git clone https://github.com/documendous/docrepox.git &&
echo "===Done.==="

echo "===Navigating to DocrepoX directory==="
cd docrepox || { echo "Failed to enter docrepox directory. Exiting."; exit 1; }

# Add hostname to DJANGO_ALLOWED_HOSTS
if grep -q "DJANGO_ALLOWED_HOSTS" env.prod.example; then
    if ! grep -q "DJANGO_ALLOWED_HOSTS=.*$hostname" env.prod.example; then
        sed -i "s/^DJANGO_ALLOWED_HOSTS=.*/&,$hostname/" env.prod.example
        echo "Added $hostname to DJANGO_ALLOWED_HOSTS."
    else
        echo "$hostname is already in DJANGO_ALLOWED_HOSTS. No changes made."
    fi
else
    # If 'DJANGO_ALLOWED_HOSTS' doesn't exist, add it with the hostname
    echo "DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1],$hostname" >> env.prod.example
    echo "Created DJANGO_ALLOWED_HOSTS with $hostname."
fi

echo "===Hostname processing complete==="

echo "===Set up Python environment==="
python -m venv .venv &&
. .venv/bin/activate &&
echo "===Done.==="

echo "===Set up dependencies==="
pip install poetry &&
poetry export --with dev -f requirements.txt --output requirements.txt &&
cp requirements.txt docrepo/requirements.txt &&
mkdir -p docrepo/mediafiles &&
cp env.prod.example .env.prod &&
cp env.prod.db.example .env.prod.db &&
cp .env.prod docrepo/.env.prod &&
echo "===Done==="

echo "===Running DocrepoX with Docker==="
docker compose -f docker-compose.prod.yml up --build
