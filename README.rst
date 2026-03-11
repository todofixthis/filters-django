.. image:: https://github.com/todofixthis/filters-django/actions/workflows/build.yml/badge.svg
   :target: https://github.com/todofixthis/filters-django/actions/workflows/build.yml
.. image:: https://readthedocs.org/projects/filters/badge/?version=latest
   :target: https://filters.readthedocs.io/en/latest/extension_filters.html#django-filters

Django Filters
==============
Adds `filters`_ for for Django-specific features, including:

- ``filters.ext.Model``: Search for a DB model instance matching the incoming
  value.


Requirements
------------
Django Filters is known to be compatible with the following Python versions:

- 3.14
- 3.13
- 3.12

Only Django v4.x is supported.

.. note::
   I'm only one person, so to keep from getting overwhelmed, I'm only committing
   to supporting the 3 most recent minor versions of Python and the most recent
   major version of Django.  Django Filters may work with versions of Python
   and/or Django not listed here — there just won't be any test coverage to
   prove it 😇

Installation
------------
This package is an extension for the `Filters library`_, so you can install it
as an extra to ``phx-filters``::

   pip install phx-filters[django]

.. important::
   Make sure to install `phx-filters`, **not** `filters`.  I created the latter
   at a previous job years ago, and after I left they never touched that project
   again and stopped responding to my emails — so in the end I had to fork it 🤷

If desired, you can install this package separately.  This allows you to control
the package version separately from ``phx-filters``::

   pip install phx-filters-django

Maintainers
-----------
To set up a local development environment:

#. `Install uv <https://docs.astral.sh/uv/getting-started/installation/>`_ (once per machine).

#. Install dependencies::

      uv sync

#. Activate pre-commit hooks::

      uv run autohooks activate --mode=pythonpath

Run tests for all supported Python versions using
`tox <https://tox.readthedocs.io/>`_::

   uv run tox -p

To run tests in the current virtualenv::

   uv run python manage.py test

Documentation
-------------
Documentation is available on `ReadTheDocs`_.

Source files for this project's documentation can be found in the
`phx-filters repo`_.

Releases
--------
.. important::

   Make sure to build releases off of the ``main`` branch, and check that all
   changes from ``develop`` have been merged before creating the release!

1. One-time setup
~~~~~~~~~~~~~~~~~
Create a `PyPI API token`_ if you don't have one, then install ``keyring`` as
a global tool and store the token:

.. code-block:: bash

    uv tool install keyring
    uv tool update-shell
    keyring set https://upload.pypi.org/legacy/ __token__

Paste your ``pypi-...`` token when prompted.

2. Publish to PyPI
~~~~~~~~~~~~~~~~~~
#. Bump the version (updates ``pyproject.toml`` and ``uv.lock``)::

    uv version <version>

#. Commit the changes::

    git add pyproject.toml uv.lock
    git commit

#. Publish to PyPI::

    uv publish --username __token__

3. Create GitHub Release
~~~~~~~~~~~~~~~~~~~~~~~~
#. Create an annotated tag and push to GitHub::

    git tag -a <version> -m "Release <version>"
    git push origin <version>

   ``<version>`` must match the updated version number in ``pyproject.toml``.

#. Go to the `Releases page for the repo`_.
#. Click ``Draft a new release``.
#. Select the tag that you created in step 1.
#. Specify the title of the release (e.g., ``Django Filters v1.2.3``).
#. Write a description for the release.  Make sure to include:
   - Credit for code contributed by community members.
   - Significant functionality that was added/changed/removed.
   - Any backwards-incompatible changes and/or migration instructions.
   - SHA256 hashes of the build artefacts.
#. GPG-sign the description for the release (ASCII-armoured).
#. Attach the build artefacts to the release.
#. Click ``Publish release``.

.. _PyPI API token: https://pypi.org/manage/account/#api-tokens
.. _filters: https://filters.readthedocs.io/
.. _Filters library: https://pypi.python.org/pypi/phx-filters
.. _phx-filters repo: https://github.com/todofixthis/filters/blob/develop/docs/extension_filters.rst
.. _ReadTheDocs: https://filters.readthedocs.io/en/latest/extension_filters.html#django-filters
.. _Releases page for the repo: https://github.com/todofixthis/filters-django/releases
