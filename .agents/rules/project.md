## Architecture

This is a `phx-filters` extension package with one filter, `Model`, in `src/filters_django/__init__.py`. It validates a value against a Django ORM query: `model` (required), `field` (default `pk`), and `**predicates`, QuerySet methods (`filter=`, `exclude=`, `select_related=` …) applied in turn. It returns the matched instance, or fails with `CODE_NOT_FOUND` or `CODE_NOT_UNIQUE`. It is registered as a `filters.extensions` entry point in `pyproject.toml`, so it is also `filters.ext.Model`.

To add a filter:

- write its class in `src/filters_django/__init__.py` and add it to `__all__`;
- register it as a `filters.extensions` entry point in `pyproject.toml`, named after the class;
- add any third-party library it needs with `uv add --bounds major <package>`.

The entry points and dependencies, and the Django test setup below, are this project's own content in the template-owned `pyproject.toml`, so edit them here.

The filters' user docs are prose in todofixthis/filters' `docs/extension_filters.rst`. A new filter needs a section there and a bullet in this repo's `README.rst`; a changed one needs its section updated wherever the change shows there. Where this session doesn't have filters checked out, list the docs change under a "Docs for todofixthis/filters" heading in the PR description, and tell the person you're working with.

## Tests

`django_test_project/` is a minimal Django project for tests only: in-memory SQLite settings and an app with the `Specie` model the tests use. It sits outside `test/` because a Python that ships the stdlib `test` package would shadow this repo's when Django or the django-stubs mypy plugin imports it, so never import Django settings or apps from `test.*`. pytest-django loads its settings through `pyproject.toml`, and mypy's django-stubs plugin through `[tool.django-stubs]`, so run mypy from the repo root.

One module per filter, `test/test_<filter>.py`, marked `pytest.mark.django_db`. Build the filter from its class (`filters_django.Model(Specie)`), not through `f.ext`, which types its classes as plain `BaseFilter` and so rejects `Model`'s arguments; one test asserts `f.ext.Model is Model`, which keeps the entry point checked.

The existing tests' multi-line docstrings predate `.agents/rules/testing.md`; write new ones to its one-line rule.
