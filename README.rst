.. image:: https://github.com/todofixthis/filters-django/actions/workflows/build.yml/badge.svg
   :target: https://github.com/todofixthis/filters-django/actions/workflows/build.yml
.. image:: https://readthedocs.org/projects/filters/badge/?version=latest
   :target: https://filters.readthedocs.io/en/latest/extension_filters.html#django-filters

Django Filters
==============
Adds `filters`_ for for Django-specific features, including:

- ``filters.ext.Model``: Search for a DB model instance matching the incoming
  value.  If you use a type checker, import it as ``filters_django.Model``
  instead.

.. important::
   Upgrading from an earlier major version? Read the guide first:

   - `Upgrading to Django Filters v5 <https://github.com/todofixthis/filters-django/blob/main/docs/upgrading_to_v5.rst>`_


Requirements
------------
Django Filters is known to be compatible with the following Python versions:

- 3.14
- 3.13
- 3.12

Only `Django LTS versions`_ are supported.

.. note::
   I'm only one person, so to keep from getting overwhelmed, I'm only committing
   to supporting the 3 most recent minor versions of Python and current Django
   LTS versions.  Django Filters may work with versions of Python
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

   uv run pytest

Documentation
-------------
Documentation is available on `ReadTheDocs`_.

Source files for this project's documentation can be found in the
`phx-filters repo`_.

Releases
--------
Steps to build releases are based on
`Packaging Python Projects Tutorial <https://packaging.python.org/en/latest/tutorials/packaging-projects/>`_.

.. important::

   Make sure to build releases off of the ``main`` branch!

One-time Setup
~~~~~~~~~~~~~~
#. Install the ``keyring`` tool and add it to your ``PATH``::

      uv tool install keyring
      uv tool update-shell

   Restart your shell after running ``update-shell``.
#. `Create a PyPI API token <https://pypi.org/manage/account/#api-tokens>`_ and store it
   in the OS keychain::

      keyring set https://upload.pypi.org/legacy/ __token__

   Paste the ``pypi-...`` token when prompted.

1. Build the Project
~~~~~~~~~~~~~~~~~~~~~
#. Set ``__version__`` in ``src/filters_django/__init__.py`` to the new version,
   and merge that change into ``main`` through ``develop``. Hatch reads the version
   from there, since ``pyproject.toml`` declares it dynamic.

#. Check out ``main`` and pull, so the build and the tag below both carry the new
   version::

      git checkout main && git pull

#. Delete artefacts from previous builds, if applicable::

    rm dist/*

#. Run the build::

    uv build

#. The build artefacts will be located in the ``dist`` directory at the top level of the
   project.

2. Upload to PyPI
~~~~~~~~~~~~~~~~~
#. Upload build artefacts to PyPI::

    uv publish --username __token__

3. Create GitHub Release
~~~~~~~~~~~~~~~~~~~~~~~~
#. Create a tag and push to GitHub::

      git tag -a <version> -m "Release <version>"
      git push origin <version>

   ``<version>`` must match ``__version__`` on ``main``.

#. Go to the `Releases page for the repo`_.
#. Click ``Draft a new release``.
#. Select the tag that you created above.
#. Specify the title of the release (e.g., ``Django Filters v1.2.3``).
#. Write a description for the release.  Make sure to include:

   - Credit for code contributed by community members.
   - Significant functionality that was added/changed/removed.
   - Any backwards-incompatible changes and/or migration instructions.
   - SHA256 hashes of the build artefacts.
#. GPG-sign the description for the release (ASCII-armoured).
#. Attach the build artefacts to the release.
#. Click ``Publish release``.

.. _Django LTS versions: https://www.djangoproject.com/download/#supported-versions
.. _filters: https://filters.readthedocs.io/
.. _Filters library: https://pypi.python.org/pypi/phx-filters
.. _phx-filters repo: https://github.com/todofixthis/filters/blob/develop/docs/extension_filters.rst
.. _ReadTheDocs: https://filters.readthedocs.io/en/latest/extension_filters.html#django-filters
.. _Releases page for the repo: https://github.com/todofixthis/filters-django/releases
