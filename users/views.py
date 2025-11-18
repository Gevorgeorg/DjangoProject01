from django.db.models import QuerySet, Count
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import User, Location
from .serializers import UserSerializer, LocationSerializer


class UserListView(ListAPIView):
    queryset: QuerySet = User.objects.annotate(
    total_ads=Count('ad')).select_related('location')
    serializer_class = UserSerializer


class UserDetailView(RetrieveAPIView):
    queryset: QuerySet = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class UserCreateView(CreateAPIView):
    queryset: QuerySet = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserUpdateView(UpdateAPIView):
    queryset: QuerySet = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class UserDeleteView(DestroyAPIView):
    queryset: QuerySet = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class LocationViewSet(ModelViewSet):
    queryset: QuerySet = Location.objects.all()
    serializer_class = LocationSerializer
