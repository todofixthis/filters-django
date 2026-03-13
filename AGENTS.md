# CLAUDE.md

## Commands

```bash
uv run autohooks activate --mode=pythonpath                      # install pre-commit hook (once per clone)
uv run git commit                                                # always use instead of git commit (runs autohooks)
uv add <package>                                                 # add a runtime dependency
uv add --group dev <package>                                     # add a dev dependency
uv run python manage.py test                                     # run tests (current virtualenv)
uv run python manage.py test test.app.test_filters_django.<Test>.<method>  # single test
uv run tox -p                                                    # test across all supported Python versions
```

## Architecture

Single-module library (`src/filters_django/__init__.py`) that extends [`phx-filters`](https://pypi.org/project/phx-filters/) with one class: `Model`.

`Model` is a `filters.BaseFilter` subclass that validates a value against a Django ORM query. Constructor args: `model` (required), `field` (default: `pk`), plus `**predicates` for arbitrary QuerySet method calls (`filter=`, `exclude=`, `select_related=`, etc.). Returns the matched instance or raises a validation error (`CODE_NOT_FOUND` / `CODE_NOT_UNIQUE`).

Registered as a `phx-filters` extension via the `filters.extensions` entry point, making it available as `filters.ext.Model`.

`test/` is a minimal Django app for testing only — in-memory SQLite, with a `Specie` model used throughout the test suite.
