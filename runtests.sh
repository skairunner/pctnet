#!/bin/sh

# This file assumes the DATABASE_URL envvar is set
python manage.sh test
pytest
