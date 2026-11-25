Upgrading to Django Filters v5
==============================
This page covers the move from Django Filters v4 to v5. If a later 5.x release
breaks something, it gets its own section on this page, headed by the version
that introduced it.

``filters.ext.Model`` returns the same model instance as in v4, and reports
the same ``not_found``, ``not_unique`` and ``exception`` error codes, with the
same messages. Most of what follows affects which ``phx-filters`` you install
and what your type checker reports. The one runtime change is the exception
type that a bad predicate raises, which shows only in the error context and
your logs.

The type-checker errors on this page are mypy's. pyright reports the same
problems in different words.

Django Filters v5 requires phx-filters v4
-----------------------------------------
Django Filters v5 depends on ``phx-filters >= 4.0.0a2``. v4 accepted
``phx-filters >= 3.4.0``. Installing Django Filters v5 upgrades
``phx-filters`` to v4, which has breaking changes of its own and adds a
runtime dependency on ``typing-extensions``.

Your ``Model`` filters need no changes for phx-filters v4. Other code that
uses phx-filters may: for example, ``some_filter | None`` now raises this
error::

   TypeError: None is not compatible with Int in a filter chain; use NoOp instead, or Optional[Int] in a type annotation.

To upgrade, follow phx-filters' guide,
`Upgrading to Filters v4 <https://filters.readthedocs.io/en/latest/upgrading_to_v4.html>`_,
before you install Django Filters v5. It lists each breaking change, its error
and its fix.

To stay on phx-filters v3, pin both packages::

   pip install 'phx-filters<4' 'phx-filters-django<5'

Type checkers now read Django Filters' annotations
--------------------------------------------------
Django Filters v5 ships a ``py.typed`` marker, so mypy and pyright check your
code against its annotations. ``Model`` is generic over the Django model it
returns: ``FilterRunner(Model(Post), value).cleaned_data`` infers ``Post``.
These changes affect only type checking.

Give ``Model`` a type argument
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Because ``Model`` is generic, mypy rejects a bare ``Model`` in an annotation
or a base class under ``--strict`` or ``disallow_any_generics``:

.. code-block:: text

   error: Missing type arguments for generic type "Model"  [type-arg]

To fix it, name the Django model::

   # Before
   post_filter: Model = Model(Post)

   # After
   post_filter: Model[Post] = Model(Post)

For a subclass meant to work with any model, declare a type parameter and
pass it on, where ``DjangoModel`` is ``django.db.models.Model``::

   class SlugModel[T: DjangoModel](Model[T]):
       ...

Call ``Model`` from ``filters_django``, not ``filters.ext``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
phx-filters types every class in the ``filters.ext`` registry as a plain
``BaseFilter``, which takes no constructor arguments. So mypy rejects any call
to ``f.ext.Model`` that passes arguments:

.. code-block:: text

   error: Too many arguments for "BaseFilter"  [call-arg]
   error: Unexpected keyword argument "field" for "BaseFilter"  [call-arg]

To fix it, import ``Model`` from ``filters_django``. It is the same class::

   # Before
   import filters as f

   f.ext.Model(Post, field="slug")

   # After
   from filters_django import Model

   Model(Post, field="slug")

Remove ``import-untyped`` ignores
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Django Filters v4 shipped no type information, so mypy reported every import
of ``filters_django`` as untyped. If you suppressed that error, mypy now
reports the suppression itself, under ``--strict`` or
``warn_unused_ignores``:

.. code-block:: text

   error: Unused "type: ignore" comment  [unused-ignore]

To fix it, delete the ``# type: ignore[import-untyped]`` comment.

A predicate that returns no ``QuerySet`` raises ``TypeError``
-------------------------------------------------------------
Each predicate you pass to ``Model``, such as ``filter=`` or
``select_related=``, must return a ``QuerySet``. When one returns something
else, such as ``count=()``, ``Model`` now raises ``TypeError``. v4 raised
``ValueError``.

You see the difference only in the ``exc`` entry of the error context and in
your logs. phx-filters reports any exception raised while applying a filter
with the ``exception`` code, so the error code is unchanged. The ``exc`` entry
now reads::

   [builtins.TypeError] Invalid result from predicate "count" (expected QuerySet, actual int).

If code or a log alert matches on ``ValueError`` here, match on ``TypeError``
instead. The fix for the predicate itself is unchanged: pass only predicates
that return a ``QuerySet``.
