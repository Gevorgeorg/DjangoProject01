from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User, Location


class UserSerializer(ModelSerializer):
    location = serializers.SlugRelatedField(read_only=True, slug_field='name')
    total_ads = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        exclude = ["password"]

    def create(self, validated_data: dict) -> User:
        user: User = User.objects.create_user(**validated_data)
        return user


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
