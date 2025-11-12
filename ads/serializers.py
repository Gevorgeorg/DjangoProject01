from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from ads.models import Ad


class AdSerializer(ModelSerializer):
    category = SlugRelatedField(read_only=True, slug_field='name')
    class Meta:

        model = Ad
        fields = '__all__'
