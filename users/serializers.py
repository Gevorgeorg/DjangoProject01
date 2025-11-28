from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer
from .models import User


class UserRegistrationSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'phone')



    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'role')


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone']
