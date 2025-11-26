from django.db.models import QuerySet, Count
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import (RetrieveAPIView,
                                     UpdateAPIView,
                                     DestroyAPIView,
                                     ListCreateAPIView,
                                     RetrieveUpdateAPIView)
from ads.permissions import IsOwnerOrAdmin
from users.models import User
from .serializers import UserSerializer, UserUpdateSerializer


class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.annotate(total_ads=Count('ad'))
    permission_classes = [AllowAny] # не обязательно так(если не укажешь будет для всех и так

    def get_serializer_class(self):
        if self.request.method == 'POST':
            from .serializers import UserRegistrationSerializer # Импорты так не хорошо!!! очень крайне редко когда надо
            return UserRegistrationSerializer
        return UserSerializer


class UserDetailView(RetrieveAPIView):
    queryset: QuerySet = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class UserUpdateView(UpdateAPIView):
    queryset: QuerySet = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    authentication_classes = [JWTAuthentication]


class UserDeleteView(DestroyAPIView):
    queryset: QuerySet = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    authentication_classes = [JWTAuthentication]


class CurrentUserView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_object(self):
        """Возвращает текущего аутентифицированного пользователя"""

        return self.request.user

    def get_serializer_class(self):
        """выбирает сериализатор в зависимости от метода"""

        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer
