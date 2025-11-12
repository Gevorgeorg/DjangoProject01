from django.db.models import QuerySet
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet
from users.models import User, Location
from .serializers import UserSerializer, LocationSerializer


class UserListView(ListAPIView):
    queryset: QuerySet = User.objects.all().select_related('location')
    serializer_class = UserSerializer


class UserDetailView(RetrieveAPIView):
    queryset: QuerySet = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(CreateAPIView):
    queryset: QuerySet = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(UpdateAPIView):
    queryset: QuerySet = User.objects.all()
    serializer_class = UserSerializer


class UserDeleteView(DestroyAPIView):
    queryset: QuerySet = User.objects.all()
    serializer_class = UserSerializer


class LocationViewSet(ModelViewSet):
    queryset: QuerySet = Location.objects.all()
    serializer_class = LocationSerializer
