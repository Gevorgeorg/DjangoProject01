import factory
from ads.models import Ad, Category
from users.models import Location
from django.contrib.auth import get_user_model

User = get_user_model()


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    name = factory.Sequence(lambda n: f"Location {n}")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    password = "testpass123"
    first_name = "Test"
    last_name = "User"
    role = "member"
    age = 25
    birth_date = "2000-01-01"
    email = factory.Sequence(lambda n: f"user{n}@test.com")
    location = factory.SubFactory(LocationFactory)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    slug = factory.Sequence(lambda n: f"cat{n}")


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = factory.Sequence(lambda n: f"Test Ad {n}")
    price = 100.500
    description = "Test description"
    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
