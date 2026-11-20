from collections.abc import Mapping, Sequence
from typing import Any

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.models import Model as DjangoModel
from django.db.models.query import QuerySet
from filters import BaseFilter

__version__ = "4.0.0"

__all__ = [
    "Model",
]


class Model[T_model: DjangoModel](BaseFilter[T_model]):
    """
    Expects the value to correspond to a record in the database.
    """

    CODE_NOT_FOUND = "not_found"
    CODE_NOT_UNIQUE = "not_unique"

    templates = {
        CODE_NOT_FOUND: "This value does not match any {model} records.",
        CODE_NOT_UNIQUE: "This value matches too many {model} records.",
    }

    def __init__(
        self,
        model: type[T_model],
        field: str = "pk",
        **predicates: Mapping[str, Any] | Sequence[Any],
    ) -> None:
        """
        Initialises the filter.

        Args:
            model: The model that will be queried.
            field: The field that the incoming value will be matched against.
            **predicates: Additional QuerySet methods to invoke to further
                limit/customise the filter result. A mapping is passed as
                keyword arguments, any other sequence as positional ones.

        Note:
            The result from calling each predicate MUST be a
            :py:class:`QuerySet`, or else an exception will be raised at
            runtime (e.g., ``count`` is not a valid predicate).

            If you specify a predicate that executes a write query (e.g.,
            ``update`` or ``delete``), the filter will still raise an
            exception... but not before executing the query!

        Example::

            f.ext.Model(
                # Find a Post record with a ``slug`` that matches the input.
                model=Post,
                field="slug",
                # Predicates
                filter={"published": True},
                exclude={"comments__isnull": True},
                select_related=("author", "comments"),
            )
        """
        super().__init__()

        self.model = model
        self.field = field
        self.predicates = predicates

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.model!r}, field={self.field!r})"

    def _apply(self, value: Any) -> T_model:
        # Queries `objects`, not `_default_manager`: the two differ for a model
        # that makes another manager its default, and this filter has always
        # queried `objects`. django-stubs types `objects` only on concrete
        # models, not on a bound type variable.
        query_set: QuerySet[T_model] = self.model.objects.filter(  # type: ignore[attr-defined]
            **{self.field: value}
        )

        for name, args in self.predicates.items():
            predicate = getattr(query_set, name)

            query_set = (
                predicate(**args) if isinstance(args, Mapping) else predicate(*args)
            )

            if not isinstance(query_set, QuerySet):
                raise TypeError(
                    f'Invalid result from predicate "{name}" '
                    f"(expected QuerySet, actual {type(query_set).__name__}).",
                )

        try:
            return query_set.get(**{self.field: value})
        # `query_set.get` raises only this model's subclasses of these.
        except ObjectDoesNotExist:
            return self._invalid_value(
                exc_info=True,
                reason=self.CODE_NOT_FOUND,
                value=value,
                template_vars={
                    "field": self.field,
                    "model": self.model.__name__,
                },
            )
        except MultipleObjectsReturned:
            return self._invalid_value(
                value=value,
                reason=self.CODE_NOT_UNIQUE,
                exc_info=True,
                template_vars={
                    "field": self.field,
                    "model": self.model.__name__,
                },
            )
