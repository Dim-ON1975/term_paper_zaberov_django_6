# Аутентификация пользователя по адресу электронной почты
from django.contrib.auth.models import User


class EmailAuthBackend:
    """
    Аутентификация посредством адреса электронной почты.
    """

    def authenticate(self, request, username=None, password=None):
        """
        Извлечение пользователя по адресу электронной почты.
        :param request: Объект, хранящий информацию о запросе, object.
        :param username: Имя пользователя, str.
        :param password: Пароль, str.
        :return: Пользователь с указанным адресом электронной почты.
        """
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        """
        Извлечение пользователя по его id.
        :param user_id: id пользователя.
        :return: Пользователь с указанным идентификатором.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
