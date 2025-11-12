from users import views
from django.urls import path

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='all_users'),
    path('users/', views.UserCreateView.as_view(), name='create_user'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='one_user'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='upd_user'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='del_user'),

    path('locations/', views.LocationView.as_view(), name='all_locations'),
    path('locations/<int:pk>/', views.LocationView.as_view(), name='one_location'),
]
