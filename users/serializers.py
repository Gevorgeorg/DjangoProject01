from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ads.models import Ad
from .models import User, Location


class UserSerializer(ModelSerializer):
    location = serializers.SlugRelatedField(read_only=True, slug_field='name')
    total_ads = serializers.SerializerMethodField()
    class Meta:
        model = User
        exclude = ["password"]

    def get_total_ads(self, obj):
        """Подсчет опубликованных объявлений пользователя"""
        return Ad.objects.filter(author=obj.username, is_published=True).count()

