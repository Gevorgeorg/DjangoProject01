from django.db.models import QuerySet
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from ads.models import Comment, Ad
from ads.permissions import IsOwnerOrAdmin
from ads.serializers import AdCreateSerializer, AdUpdateSerializer, AdListSerializer, AdDetailSerializer, \
    CommentCreateUpdateSerializer, CommentSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication


class AdListCreateAPIView(ListCreateAPIView):
    serializer_class = AdListSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdCreateSerializer
        return AdListSerializer

    def get_queryset(self) -> QuerySet[Ad]:
        """Фильтры"""

        queryset: QuerySet = Ad.objects.all().select_related('author')

        search_text: str = self.request.GET.get('title')
        if search_text:
            queryset: QuerySet = queryset.filter(title__icontains=search_text)

        return queryset

    def perform_create(self, serializer):
        """Автоматически назначает текущего пользователя автором объявления"""

        serializer.save(author=self.request.user)


class MyAdsListView(ListAPIView):
    serializer_class = AdListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ad.objects.filter(author=self.request.user).select_related('author').order_by('-created_at')


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all().select_related('author')
    serializer_class = AdDetailSerializer


class AdUpdateView(UpdateAPIView):
    queryset: QuerySet = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    authentication_classes = [JWTAuthentication]


class AdDeleteView(DestroyAPIView):
    queryset: QuerySet = Ad.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    authentication_classes = [JWTAuthentication]


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommentCreateUpdateSerializer
        return CommentSerializer

    def get_queryset(self):
        """Комментарии для конкретного объявления"""

        return Comment.objects.filter(
            ad_id=self.kwargs['ad_pk']
        ).select_related('author', 'ad').order_by('-created_at')

    def perform_create(self, serializer):
        """Автоматическое связывание с объявлением и автором"""
        ad = get_object_or_404(Ad, pk=self.kwargs['ad_pk'])
        serializer.save(author=self.request.user, ad=ad)
