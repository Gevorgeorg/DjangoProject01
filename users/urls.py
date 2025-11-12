from rest_framework import routers

from users import views
from django.urls import path

simple_router = routers.SimpleRouter()
simple_router.register('locations', views.LocationViewSet)

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='All_users'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='one_user'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='upd_user'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='del_user'),

]

urlpatterns += simple_router.urls
