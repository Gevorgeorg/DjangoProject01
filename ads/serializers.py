from rest_framework.relations import SlugRelatedField
from ads.models import Selection, Ad
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class AdSerializer(ModelSerializer):
    category = SlugRelatedField(read_only=True, slug_field='name')
    author = SlugRelatedField(read_only=True, slug_field='first_name')

    class Meta:
        model = Ad
        fields = '__all__'


class AdCreateSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = ['name', 'price', 'description', 'is_published', 'category', 'image']

    def create(self, validated_data: dict) -> Ad:
        return Ad.objects.create(
            **validated_data,
            author=self.context['request'].user
        )


class AdUpdateSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = ['name', 'price', 'description', 'is_published', 'category', 'image']


class SelectionSerializer(serializers.ModelSerializer):
    items = AdSerializer(many=True, read_only=True)
    author = serializers.IntegerField(source='author.id', read_only=True)
    items_input = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Selection
        fields = ['id', 'name', 'items', 'author', 'items_input']

    def create(self, validated_data):
        items_data: list[int] = validated_data.pop('items_input', [])
        selection: Selection = Selection.objects.create(**validated_data,
                                                        author=self.context['request'].user)
        selection.items.set(Ad.objects.filter(id__in=items_data))
        return selection

    def update(self, instance, validated_data):
        items_data: list[int] = validated_data.pop('items_input', None)

        instance.name = validated_data.get('name', instance.name)
        instance.save()

        if items_data is not None:
            instance.items.set(Ad.objects.filter(id__in=items_data))

        return instance
