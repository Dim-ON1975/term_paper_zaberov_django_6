from django.urls import path, include
from . import views
from .apps import AccountConfig
from .views import ProfileDetailView, UserDeleteView

app_name = AccountConfig.name

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
]
