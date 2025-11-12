from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ads.models import Ad
from .models import User, Location


class UserSerializer(ModelSerializer):
    location = serializers.CharField(source='location.name', read_only=True)
    total_ads = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ["password"]

    def get_total_ads(self, obj: User) -> int:
        """Подсчет постов авторов"""

        return Ad.objects.filter(author=obj, is_published=True).count()


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
