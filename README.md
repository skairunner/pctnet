# PCTNet

[![Build Status](https://travis-ci.org/skairunner/pctnet.svg?branch=master)](https://travis-ci.org/skairunner/pctnet)
[![Coverage Status](https://coveralls.io/repos/github/skairunner/pctnet/badge.svg?branch=master)](https://coveralls.io/github/skairunner/pctnet?branch=master)

PCTNet is an free, open-source fanfic community platform, with integrated story archive, interested-based groups and group forums. We hope to provide a fandom-friendly platform that can be self-hosted and provides dedicated space for a fandom to live in. The current design is heavily inspired by fimfiction.net, though it shares no code.

## Installing

Ensure you have a PostgreSQL installation that can be pointed to by the following database url:
```
postgres://pctnetuser:tTdkrHSzijCw4JjepJ4u@localhost:5432/pctnet
```

That is, a user named pctnetuser with the password `tTdkrHSzijCw4JjepJ4u` should be available on the localhost at port 5432, and there must be a database named `pctnet`.

In the root directory, run the following to install dependencies:
```
$ pipenv install
```

You can subsequently use `pipenv shell` to enter the virtual environment.

On the first installation, or when a model is updated, run the following:
```
$ ./manage.sh makemigrations
$ ./manage.sh migrate
```

You can run the server with this command:
```
$ ./manage.sh runserver 127.0.0.1:8000
```
The server will recompile and rerun whenever a watched file is edited.
