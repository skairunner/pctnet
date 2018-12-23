# PCTNet

[![Build Status](https://travis-ci.org/skairunner/pctnet.svg?branch=master)](https://travis-ci.org/skairunner/pctnet)
[![Coverage Status](https://coveralls.io/repos/github/skairunner/pctnet/badge.svg?branch=master)](https://coveralls.io/github/skairunner/pctnet?branch=master)

PCTNet is an free, open-source fanfic community platform, with integrated story archive, interest-based groups and group forums. We hope to provide a fandom-friendly platform that can be self-hosted and provides dedicated space for a fandom to live in. The current design is heavily inspired by fimfiction.net, though it shares no code.

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

## Testing
There are two kinds of tests in this repo.
### Django tests
Django tests are based on Webtest, which is a `unittest`-style WSGI test framework that provides easy-to-use functional testing on webapps. To run tests, the command is:
```
$ ./manage.sh test [app]
```
So to test stories, you run `./manage.sh test stories`. If you don't provide [app], you run all Django tests.

### Pytest
Currently only the `sanitizer` module uses pytest, a Pythonic, syntax-light, user-friendly testing framework. Pytest auto-discovers tests in files named `test_*.py` or `tests.py`. To run tests, simply execute
```
$ pytest
```

## Contributing
Any contributions are highly welcome. Many of the Issues are good starts, and the Public project's Narrow Scope column in particular are tasks that shouldn't have very wide-reaching repurcussions.

As typical for an open source project, you can contribute by forking this repo on Github, implementing your changes in your repo, then making a pull request to skairunner/PCTNet. Remember to run tests to make sure you didn't cause regressions. Also good practice is writing tests for features you've made or bugs that have been fixed.

When contributing, it is helpful to format commits like this:
```
[Type]: [which part] [description]
```
So if you fixed a bug that causes chapters to be displayed upside down, you might write:
```
Fix: Chapter display inverted
```
Other types include Feat (for features) and Meta for adding tests. Additionally, if the bug/feature is referenced in an issue, add the issue to the comment as `#<issue id>`. You can also add the issue to the pull request.
