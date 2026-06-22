#!/usr/bin/env bash
set -o errexit

python -m pip install -r my_blog/requirements.txt
python my_blog/manage.py collectstatic --noinput
