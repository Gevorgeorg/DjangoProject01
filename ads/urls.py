from ads import views
from django.urls import path

urlpatterns = [
    path('', views.home_view, name='ads_home'),
    path('ads/', views.AdView.as_view(), name='all_ads'),
    path('ads/<int:pk>/', views.AdEntityView.as_view(), name='one_ad'),
    path('categories/', views.CategoryListView.as_view(), name='all_categories'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='one_category'),

]
