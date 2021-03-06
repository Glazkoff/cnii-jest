#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

python manage.py migrate
python manage.py collectstatic --noinput --verbosity 0
python manage.py loaddata admin_interface_theme_cnii_jest.json
python manage.py loaddata settings.json
python manage.py runserver 0.0.0.0:8003