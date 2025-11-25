from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'ads/(?P<ad_pk>\d+)/comments', views.CommentViewSet, basename='comment')
urlpatterns = [

    path('ads/', views.AdListCreateAPIView.as_view(), name='all_ads'),
    path('ads/me/', views.MyAdsListView.as_view(), name='my_ads'),

    path('ads/<int:pk>/', views.AdDetailView.as_view(), name='one_ad'),
    path('ads/<int:pk>/update/', views.AdUpdateView.as_view(), name='update_ad'),
    path('ads/<int:pk>/delete/', views.AdDeleteView.as_view(), name='delete_ad'),
    path('', include(router.urls)),
]
