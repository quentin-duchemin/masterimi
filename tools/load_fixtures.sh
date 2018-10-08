#!/bin/bash
set -o nounset
set -o errexit
set -o xtrace
set -o pipefail

docker-compose exec back /venv/bin/python manage.py loaddata /app/parcours_imi/fixtures/constraints.json
docker-compose exec back /venv/bin/python manage.py loaddata /app/parcours_imi/fixtures/masters.json
docker-compose exec back /venv/bin/python manage.py loaddata /app/parcours_imi/fixtures/courses_imi.json
docker-compose exec back /venv/bin/python manage.py loaddata /app/parcours_imi/fixtures/courses_mva_s1.json
docker-compose exec back /venv/bin/python manage.py loaddata /app/parcours_imi/fixtures/courses_mva_s2.json
docker-compose exec back /venv/bin/python manage.py loaddata /app/parcours_imi/fixtures/courses_mpro.json
