from django.urls import path, include
from . import views
from .apps import AccountConfig
from .views import RegisterView, ProfileUpdateView, ProfileDetailView, UserDeleteView, EmailVerify, MyLoginView, \
    MyPasswordChangeDoneView, MyPasswordChangeView, MyPasswordResetView, MyPasswordResetDoneView, \
    MyPasswordResetConfirmView, MyPasswordResetCompleteView
from django.contrib.auth.views import TemplateView, LogoutView

app_name = AccountConfig.name

urlpatterns = [
    # Авторизация
    path('', MyLoginView.as_view(), name='login'),
    # Выход
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    # Сообщение об отправке на почту подтверждения
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),
    # Подтверждение email
    path('confirm_email/', TemplateView.as_view(template_name='account/confirm_email.html'),
         name='confirm_email'),
    # Некорректный токен
    path('invalid_verify/', TemplateView.as_view(template_name='account/invalid_verify.html'),
         name='invalid_verify'),
    path('', include('django.contrib.auth.urls')),
    # Редактирование профиля
    path('update_profile/', ProfileUpdateView.as_view(), name='update_profile'),
    # Просмотр профиля
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    # Удаление профиля
    path('delete_profile/', UserDeleteView.as_view(), name='user_delete'),
    # Смена пароля
    path('password-change/', MyPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', MyPasswordChangeDoneView.as_view(), name='password_change_done'),
    # Сброс пароля
    path('password-reset/', MyPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/complete/', MyPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
