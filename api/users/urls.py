from django.urls import path
from .views import UsersAPIView, UserDetailAPIView, UsersCreateAPIView, UsersUpdateAPIView, UsersDeleteAPIView

urlpatterns = [
    path('list/', UsersAPIView.as_view(), name='user-list'),
    path('-create/', UsersCreateAPIView.as_view(), name='users-create'),
    path('-detail/<uuid:guid>/', UsersDeleteAPIView.as_view(), name='users-detail'),
    path('-update/<uuid:guid>/', UsersUpdateAPIView.as_view(), name='users-detail'),
    path('-delete/<uuid:guid>/', UserDetailAPIView.as_view(), name='users-detail'),
]
