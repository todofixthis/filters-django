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

- 3.12
- 3.11
- 3.10

Only Django v4.x is supported.

.. note::
   I'm only one person, so to keep from getting overwhelmed, I'm only committing
   to supporting the 3 most recent minor versions of Python and the most recent
   major version of Django.  Django Filters may work with versions of Python
   and/or Django not listed here — there just won't be any test coverage to
   prove it 😇

If you encounter any issues, please report them on the project's `Bug Tracker`_,
and be sure to indicate which version of Django you are using.

Installation
------------
This package is an extension for the `Filters library`_, so you can install it
as an extra to ``phx-filters``:

.. code:: bash

   pip install phx-filters[django]

.. important::
   Make sure to install `phx-filters`, **not** `filters`.  I created the latter
   at a previous job years ago, and after I left they never touched that project
   again and stopped responding to my emails — so in the end I had to fork it 🤷

If desired, you can install this package separately.  This allows you to control
the package version separately from ``phx-filters``.

.. code:: bash

   pip install phx-filters-django


Running Unit Tests
------------------
Install the package with the ``test-runner`` extra to set up the necessary
dependencies, and then you can run the tests with the ``tox`` command::

   pip install -e .[test-runner]
   tox -p

To run tests in the current virtualenv::

   python manage.py test

Documentation
-------------
Documentation is available on `ReadTheDocs`_.

Source files for this project's documentation can be found in the
`phx-filters repo`_.

Releases
--------
Steps to build releases are based on `Packaging Python Projects Tutorial`_

.. important::

   Make sure to build releases off of the ``main`` branch, and check that all
   changes from ``develop`` have been merged before creating the release!

1. Build the Project
~~~~~~~~~~~~~~~~~~~~
#. Install extra dependencies (you only have to do this once)::

    pip install -e '.[build-system]'

#. Delete artefacts from previous builds, if applicable::

    rm dist/*

#. Run the build::

    python -m build

#. The build artefacts will be located in the ``dist`` directory at the top
   level of the project.

2. Upload to PyPI
~~~~~~~~~~~~~~~~~
#. `Create a PyPI API token`_ (you only have to do this once).
#. Increment the version number in ``pyproject.toml``.
#. Check that the build artefacts are valid, and fix any errors that it finds::

    python -m twine check dist/*

#. Upload build artefacts to PyPI::

    python -m twine upload dist/*


3. Create GitHub Release
~~~~~~~~~~~~~~~~~~~~~~~~
#. Create a tag and push to GitHub::

    git tag <version>
    git push

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

.. _Bug Tracker: https://github.com/todofixthis/filters-django/issues
.. _Create a PyPI API token: https://pypi.org/manage/account/token/
.. _filters: http://filters.readthedocs.io/
.. _Filters library: https://pypi.python.org/pypi/phx-filters
.. _Packaging Python Projects Tutorial: https://packaging.python.org/en/latest/tutorials/packaging-projects/
.. _phx-filters repo: https://github.com/todofixthis/filters/blob/develop/docs/extension_filters.rst
.. _ReadTheDocs: https://filters.readthedocs.io/en/latest/extension_filters.html#django-filters
.. _Releases page for the repo: https://github.com/todofixthis/filters-django/releases
.. _tox: https://tox.readthedocs.io/
