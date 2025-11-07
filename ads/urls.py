from ads import views
from django.urls import path

from ads.views import CategoryUpdateView, CategoryDeleteView, AdUploadImageView

urlpatterns = [
    path('', views.home_view, name='home'),
    path('ads/', views.AdView.as_view(), name='all_ads'),
    path('ads/<int:pk>/', views.AdView.as_view(), name='one_ad'),
    path('ad/<int:pk>/upload_image/', AdUploadImageView.as_view(), name='ad-upload-image'),
    path('categories/', views.CategoryListView.as_view(), name='all_categories'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='one_category'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
]
