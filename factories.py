import factory

import models


class UserFactory(factory.Factory):
    """Factory for User instance."""

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    phone = factory.Faker("pyint", max_value=9999999999)
    email = factory.Faker("email")
    passport_id = factory.Faker("pyint")
    passport_series = factory.Faker("pyint", max_value=999999)

    class Meta:
        model = models.User
