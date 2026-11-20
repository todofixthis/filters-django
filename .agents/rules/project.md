## Architecture

This is a `phx-filters` extension package. Its filters live in `src/filters_django/__init__.py`, each registered as a `filters.extensions` entry point in `pyproject.toml`, so `Model` is also `filters.ext.Model`. `Model` validates a value against a Django ORM query: `model` (required), `field` (default `pk`), and `**predicates`, QuerySet methods (`filter=`, `exclude=`, `select_related=` …) applied in turn. It returns the matched instance, or fails with `CODE_NOT_FOUND` or `CODE_NOT_UNIQUE`.

To add a filter:

- write its class in `src/filters_django/__init__.py` and add it to `__all__`;
- register it as a `filters.extensions` entry point in `pyproject.toml`, named after the class;
- add any third-party library it needs with `uv add --bounds major <package>`.

The entry points and dependencies, the mypy plugin and override, the RUF012 ignore, and the Django test setup below are this project's own content in the template-owned `pyproject.toml`, so edit them here.

The filters' user docs are prose in todofixthis/filters' `docs/extension_filters.rst`. A new filter needs a section there and a bullet in this repo's `README.rst`; a changed one needs its section updated wherever the change shows there. Where this session doesn't have filters checked out, list the docs change under a "Docs for todofixthis/filters" heading in the PR description, and tell the person you're working with.

## Tests

`django_test_project/` is a minimal Django project for tests only: in-memory SQLite settings, and an app whose `models.py` holds the models the tests use. Add a test model or field there; pytest-django creates the tables without migrations, so don't add any. `rg django_test_project` finds every place that names the package, should it move.

It sits outside `test/` because a Python that ships the stdlib `test` package hides this repo's `test` package from the django-stubs mypy plugin, which crashed mypy there. uv's own Python builds leave that package out, so the crash won't reproduce under them; never move Django settings or apps back under `test/`.

The plugin imports `django_test_project.settings` by module path, so run mypy from the repo root. From a subdirectory it fails with `Error constructing plugin instance of NewSemanalDjangoPlugin` (an `INTERNAL ERROR` asking you to try mypy master, over `ModuleNotFoundError: No module named 'django_test_project'`), which is not a mypy bug. pytest runs from anywhere: its `pythonpath` is resolved against the repo root.

One module per filter, `test/test_<filter>.py`, marked `pytest.mark.django_db`. Build the filter from its class (`filters_django.Model(Specie)`), not through `f.ext`, which types its classes as plain `BaseFilter` and so rejects their arguments. Each module asserts its filter's entry point once (`assert f.ext.Model is Model`), the only check that the entry point resolves.

The existing tests' multi-line docstrings predate `.agents/rules/testing.md`; write new ones to its one-line rule.
