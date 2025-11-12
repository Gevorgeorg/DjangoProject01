from rest_framework.relations import SlugRelatedField
from ads.models import Ad
from rest_framework.serializers import ModelSerializer


class AdSerializer(ModelSerializer):
    category = SlugRelatedField(read_only=True, slug_field='name')
    author = SlugRelatedField(read_only=True, slug_field='first_name')

    class Meta:
        model = Ad
        fields = '__all__'


class AdCreateSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = ['name', 'author', 'price', 'description', 'is_published', 'category', 'image']

    def create(self, validated_data: dict) -> Ad:
        return Ad.objects.create(**validated_data)


class AdUpdateSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = ['name', 'price', 'description', 'is_published', 'category', 'image']
