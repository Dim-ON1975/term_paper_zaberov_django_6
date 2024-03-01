from account.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, CreateView, View, UpdateView, DetailView

from .forms import AuthenticationForm, UserRegisterForm, UserProfileForm

from django.contrib.auth.views import LoginView, PasswordChangeDoneView, PasswordChangeView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from core.settings import LOGIN_REDIRECT_URL
from .services import send_email_for_verify
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.exceptions import ValidationError
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from core.settings import LOGIN_URL



class DataMixin:
    paginate_by = 5


class RedirectPermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = None
    login_url = reverse_lazy('clients:error403')

    def handle_no_permission(self):
        return redirect(self.get_login_url())


class MyLoginView(LoginView):
    """Авторизация"""
    form_class = AuthenticationForm

    def form_valid(self, form):
        form.save()
        cd = form.cleaned_data
        # аутентификация: возвращается объект "user"
        user = authenticate(self.request,
                            username=cd['username'],
                            password=cd['password'])
        if user is not None:
            # если user существует, то проверяется его активность
            if user.is_active:
                login(self.request, user)
                return HttpResponse('Аутентификация прошла успешно')
            else:
                return HttpResponse('Отключенная учетная запись')
        return redirect(LOGIN_REDIRECT_URL)

    def form_invalid(self, form):
        return HttpResponse('Неверный логин')


class RegisterView(CreateView):
    """Регистрация"""
    model = User
    form_class = UserRegisterForm
    template_name = 'account/register.html'

    def form_valid(self, form):
        form.save()
        user = authenticate(
            email=form.cleaned_data.get('email'),
            password=form.cleaned_data.get('password1')
        )
        send_email_for_verify(self.request, user)
        return redirect('account:confirm_email')


class EmailVerify(View):
    """Верификация почты при регистрации"""

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('clients:home')
        return redirect('account:invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() декодирует в байт-строку
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
                TypeError,
                ValueError,
                OverflowError,
                User.DoesNotExist,
                ValidationError,
        ):
            user = None
        return user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля"""
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('account:profile')

    def get_object(self, queryset=None):
        return self.request.user


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """Просмотр профиля"""
    model = User
    success_url = reverse_lazy('account:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление пользователя"""
    model = User
    success_url = reverse_lazy('account:login')

    def get_object(self, queryset=None):
        return self.request.user


class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy("account:password_change_done")
    template_name = "account/password_change_form.html"


class MyPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = "account/password_change_done.html"


class MyPasswordResetView(PasswordResetView):
    email_template_name = "account/password_reset_email.html"
    success_url = reverse_lazy("account:password_reset_done")
    template_name = "account/password_reset_form.html"


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = "account/password_reset_done.html"


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("account:password_reset_complete")
    template_name = "account/password_reset_confirm.html"


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "account/password_reset_complete.html"


class UserListView(RedirectPermissionRequiredMixin, DataMixin, ListView):
    model = User
    permission_required = 'account.view_user'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser:
            queryset = queryset.order_by("-is_superuser", "-is_staff", "-is_active", "last_name", "first_name",
                                         "email").distinct()
        return queryset


@login_required
@user_passes_test(lambda u: lambda user_id: u == get_object_or_404(User, pk=user_id).user,
                  login_url=LOGIN_URL)
def toggle_activity(request, pk):
    """ Активация/деактивация пользователей """
    user_item = get_object_or_404(User, pk=pk)
    if user_item.is_active:
        user_item.is_active = False
    else:
        user_item.is_active = True

    user_item.save()

    return redirect(reverse('account:user_list'))
