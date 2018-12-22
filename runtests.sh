#!/bin/sh

# This file assumes the DATABASE_URL envvar is set
coverage run manage.py test
coverage run --append -m pytest
