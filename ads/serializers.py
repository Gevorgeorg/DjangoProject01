from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Ad, Comment


class AdListSerializer(ModelSerializer):
    pk = serializers.IntegerField(source='id', read_only=True)
    author_first_name = serializers.CharField(source='author.first_name', read_only=True)
    author_last_name = serializers.CharField(source='author.last_name', read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    phone = serializers.CharField(source='author.phone', read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'


class AdDetailSerializer(ModelSerializer):
    author_first_name = serializers.CharField(source='author.first_name', read_only=True)
    author_last_name = serializers.CharField(source='author.last_name', read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    phone = serializers.CharField(source='author.phone', read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'


class AdCreateSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = ['image', 'title', 'price', 'description']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data['created_at'] = timezone.now()
        return super().create(validated_data)


class AdUpdateSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = ['image', 'title', 'price', 'description']


class CommentSerializer(ModelSerializer):
    pk = serializers.IntegerField(source='id', read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    author_first_name = serializers.CharField(source='author.first_name', read_only=True)
    author_last_name = serializers.CharField(source='author.last_name', read_only=True)
    ad_id = serializers.IntegerField(source='ad.id', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'pk', 'text', 'author_id', 'created_at',
            'author_first_name', 'author_last_name', 'ad_id'
        ]


class CommentCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text']
