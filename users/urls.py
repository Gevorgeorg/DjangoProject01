from users import views
from django.urls import path

urlpatterns = [
    path('users/', views.UserView.as_view(), name='all_users'),
    path('users/<int:pk>/', views.UserView.as_view(), name='one_user'),
    path('locations/', views.LocationView.as_view(), name='all_locations'),
    path('locations/<int:pk>/', views.LocationView.as_view(), name='one_location'),
]
