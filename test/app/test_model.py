"""
Note: most of the animals referenced in these tests are cuddly because,
let's face it, those are more fun to research (:
"""

import pytest
import filters as f

from test.app.models import Specie

pytestmark = pytest.mark.django_db


def test_pass_none():
    """
    ``None`` always passes this filter.

    Chain with ``Required`` to reject null values.
    """
    runner = f.FilterRunner(f.ext.Model(Specie), None)
    assert not runner.has_exceptions
    assert runner.is_valid()
    assert runner.cleaned_data is None


def test_pass_pk_match():
    """
    The incoming value matches the PK of an existing record.
    """
    # noinspection SpellCheckingInspection
    target_specie = Specie.objects.create(
        binomial_name="Mesocricetus Auratus",
        common_name="Golden Hamster",
        is_cuddly=True,
    )

    runner = f.FilterRunner(f.ext.Model(Specie), target_specie.pk)
    assert not runner.has_exceptions
    assert runner.is_valid()
    assert isinstance(runner.cleaned_data, Specie)
    assert runner.cleaned_data == target_specie


def test_fail_no_pk_match():
    """
    The incoming value does not match the PK of any existing records.
    """
    runner = f.FilterRunner(f.ext.Model(Specie), 42)
    assert not runner.has_exceptions
    assert not runner.is_valid()
    assert runner.error_codes == {"": [f.ext.Model.CODE_NOT_FOUND]}


def test_pass_alternate_field_match():
    """
    You can configure the constraint to match a value other than PK.
    """
    # noinspection SpellCheckingInspection
    target_specie = Specie.objects.create(
        binomial_name="Setonix Brachyurus",
        common_name="Quokka",
        is_cuddly=False,
    )

    runner = f.FilterRunner(f.ext.Model(Specie, field="common_name"))

    runner.apply(target_specie.common_name)
    assert not runner.has_exceptions
    assert runner.is_valid()
    assert isinstance(runner.cleaned_data, Specie)
    assert runner.cleaned_data == target_specie

    # Note that we specified ``common_name`` as the match field, so PK no
    # longer works.
    runner.apply(target_specie.pk)
    assert not runner.has_exceptions
    assert not runner.is_valid()
    assert runner.error_codes == {"": [f.ext.Model.CODE_NOT_FOUND]}


def test_fail_too_many_matches():
    """
    The incoming value matches more than one record.
    """
    # noinspection SpellCheckingInspection
    Specie.objects.create(
        binomial_name="Enhydra Lutris",
        common_name="Sea Otter",
        is_cuddly=True,
    )

    # noinspection SpellCheckingInspection
    Specie.objects.create(
        binomial_name="Aix Galericulata",
        common_name="Mandarin Duck",
        is_cuddly=True,
    )

    runner = f.FilterRunner(f.ext.Model(Specie, field="is_cuddly"))

    runner.apply(True)
    assert not runner.has_exceptions
    assert not runner.is_valid()
    assert runner.error_codes == {"": [f.ext.Model.CODE_NOT_UNIQUE]}


# noinspection SpellCheckingInspection
def test_predicates():
    """
    You can use ``predicates`` to specify additional filters to add to the
    query.
    """
    target_specie = Specie.objects.create(
        binomial_name="Bradypus Pygmaeus",
        common_name="Dwarf Sloth",
        is_cuddly=True,
    )

    # Note that without any predicates, the filter will find our specie
    # just fine.
    runner = f.FilterRunner(f.ext.Model(Specie), target_specie.pk)
    assert not runner.has_exceptions
    assert runner.is_valid()
    assert isinstance(runner.cleaned_data, Specie)
    assert runner.cleaned_data == target_specie

    # However, if we add a predicate that restricts the search to
    # non-cuddlies, the input is no longer valid.
    runner = f.FilterRunner(
        f.ext.Model(Specie, filter={"is_cuddly": False}),
        target_specie.pk,
    )
    assert not runner.has_exceptions
    assert not runner.is_valid()
    assert runner.error_codes == {"": [f.ext.Model.CODE_NOT_FOUND]}


def test_error_predicate_invalid():
    """
    Predicates must return :py:class:`django.db.models.query.QuerySet`
    objects, or else they are invalid.
    """
    # noinspection SpellCheckingInspection
    target_specie = Specie.objects.create(
        binomial_name="Allactaga Tetradactyla",
        common_name="Jerboa",
        # I honestly can't tell.
        is_cuddly=None,
    )

    runner = f.FilterRunner(
        # ``QuerySet.count()`` does not return a ``QuerySet`` instance, so
        # it is not a valid predicate.
        f.ext.Model(Specie, count=()),
        target_specie.pk,
    )
    assert runner.has_exceptions
    assert not runner.is_valid()
    assert runner.cleaned_data is None
    assert runner.error_codes == {"": [f.BaseFilter.CODE_EXCEPTION]}


def test_pass_predicate_side_effects():
    """
    Reckless use of predicates that trigger write queries may result in
    side effects.
    """
    # noinspection SpellCheckingInspection
    target_specie = Specie.objects.create(
        binomial_name="Otolemur Crassicaudatus",
        common_name="Galago",
        is_cuddly=True,
    )

    runner = f.FilterRunner(
        f.ext.Model(Specie, update={"is_cuddly": False}),
        target_specie.pk,
    )
    assert runner.has_exceptions
    assert not runner.is_valid()
    assert runner.cleaned_data is None
    assert runner.error_codes == {"": [f.BaseFilter.CODE_EXCEPTION]}

    # An exception was raised... but not before the DB record was
    # updated!
    assert not Specie.objects.get(pk=target_specie.pk).is_cuddly
