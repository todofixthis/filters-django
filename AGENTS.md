# CLAUDE.md

## Git

Always use `uv run git commit` (not `git commit`) so that autohooks run correctly. The `creative-commits` skill still applies.

## Commands

```bash
uv run tox -p                                                    # all Python versions, parallel
uv run python manage.py test                                     # current virtualenv only
uv run python manage.py test test.app.test_filters_django.<Test>.<method>  # single test
```

## Architecture

Single-module library (`src/filters_django/__init__.py`) that extends [`phx-filters`](https://pypi.org/project/phx-filters/) with one class: `Model`.

`Model` is a `filters.BaseFilter` subclass that validates a value against a Django ORM query. Constructor args: `model` (required), `field` (default: `pk`), plus `**predicates` for arbitrary QuerySet method calls (`filter=`, `exclude=`, `select_related=`, etc.). Returns the matched instance or raises a validation error (`CODE_NOT_FOUND` / `CODE_NOT_UNIQUE`).

Registered as a `phx-filters` extension via the `filters.extensions` entry point, making it available as `filters.ext.Model`.

`test/` is a minimal Django app for testing only — in-memory SQLite, with a `Specie` model used throughout the test suite.
