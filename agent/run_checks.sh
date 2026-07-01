#!/bin/bash
# agent/run_checks.sh

set -e   # stop immediately if any command fails

echo "================================"
echo " STEP 1: Building containers"
echo "================================"
docker compose build

echo "================================"
echo " STEP 2: Starting containers"
echo "================================"
docker compose up -d

echo "Waiting for MySQL to be ready..."
sleep 10

echo "================================"
echo " STEP 3: Django system checks"
echo "================================"
docker compose exec web python manage.py check

echo "================================"
echo " STEP 4: Running migrations"
echo "================================"
docker compose exec web python manage.py migrate

echo "================================"
echo " STEP 5: Running test suite"
echo "================================"
docker compose exec web python manage.py test

echo "================================"
echo " STEP 6: Security scan (bandit)"
echo "================================"
docker compose exec web bandit -r . -x ./tests,./migrations || true

echo "================================"
echo " STEP 7: Dependency vulnerability scan"
echo "================================"
docker compose exec web safety check || true

echo "================================"
echo " ALL CHECKS COMPLETE"
echo "================================"

docker compose down