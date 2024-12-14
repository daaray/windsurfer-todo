"""Factories for Todo app tests."""

import factory
from factory.django import DjangoModelFactory

from ..models import Todo


class TodoFactory(DjangoModelFactory):
    """Factory for Todo model."""

    class Meta:
        """Factory configuration."""

        model = Todo

    title = factory.Faker("sentence", nb_words=4)
    completed = factory.Faker("boolean")
    order = factory.Sequence(lambda n: n)
