from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from .models import User, Location

from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

class MinAgeValidator:
    """Валидатор минимального возраста"""

    def __init__(self, min_age=9):
        self.min_age = min_age

    def __call__(self, value):
        min_birth_date = timezone.now().date() - timedelta(days=self.min_age * 365)

        if value > min_birth_date:
            raise ValidationError(f'Регистрация разрешена только с {self.min_age} лет')


class UserSerializer(ModelSerializer):
    location = serializers.SlugRelatedField(read_only=True, slug_field='name')
    total_ads = serializers.IntegerField(read_only=True)
    birth_date = serializers.DateField(validators=[MinAgeValidator(9)])

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data: dict) -> User:
        user: User = User.objects.create_user(**validated_data)
        return user


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
