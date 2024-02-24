from django import forms
from account.models import User

from account.services import send_email_for_verify
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate


class AuthenticationForm(DjangoAuthenticationForm):
    """ Форма аутентификации пользователя с проверкой верификации почты"""

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )

            # Если такого пользователя не существует
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

            # Если электронная почта не верифицирована
            if not self.user_cache.email_verify:
                # Отправляем письмо, содержащее ссылку для верификации
                send_email_for_verify(self.request, self.user_cache)
                # Выводим сообщение
                raise ValidationError(
                    'Электронная почта не верифицирована. Ссылка для верификации выслана по email.',
                    code='invalid_login',
                )

        return self.cleaned_data


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'country', 'email', 'phone', 'date_of_birth', 'avatar',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()
