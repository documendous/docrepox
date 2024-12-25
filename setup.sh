#!/usr/bin/env bash

echo "*  Cloning DocrepoX repository ...  *"
git clone https://github.com/documendous/docrepox.git &&
echo "*  Done.  *"

echo "* Set up Python environment ...  *"
cd docrepox &&
python -m venv .venv &&
. .venv/bin/activate &&
echo "*  Done.  *"

echo "*  Set up dependencies ... *"
pip install poetry &&
# poetry install &&
poetry export --with dev -f requirements.txt --output requirements.txt &&
cp requirements.txt docrepo/requirements.txt &&
mkdir docrepo/mediafiles &&
cp env.prod.example .env.prod &&
cp env.prod.db.example .env.prod.db &&
cp .env.prod docrepo/.env.prod &&
echo "*  Done.  "

echo "* Running DocrepoX with Docker ...  *"
docker compose -f docker-compose.prod.yml up --build
