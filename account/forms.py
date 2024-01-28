from django import forms
from django.contrib.auth.models import User

from account.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    """
    Модельная форма для модели пользователя при его регистрации.
    """
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)  # Установить пароль
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)  # Подтвердить пароль

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

    def clean_password2(self):
        """
        Валидация полей формы, проверяющая, что оба пароля одинаковые.
        Выдаёт ошибку валидации, если пароли не совпадают.
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

    def clean_email(self):
        """
        Не позволяет пользователям регистрироваться
        с одинаковым адресом электронной почты.
        """
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Пользователь с таким email уже зарегистрирован')
        return data


class UserEditForm(forms.ModelForm):
    """
    Форма редактирования имени, фамилии и адреса электронной почты.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Этот email уже используется.')
        return data


class ProfileEditForm(forms.ModelForm):
    """
    Форма редактирования даты рождения и фотографии.
    """
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo',)
