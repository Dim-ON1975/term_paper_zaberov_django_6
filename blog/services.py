from django.core.mail import send_mail
from core import settings


def sending_mail(title: str, email: str):
    """ Отправка письма по электронной почте """
    send_mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        subject='Ура! Сотый просмотр Вашего поста!',
        message=f'Поздравляем! Ваш пост "{title}" набирает популярность! Его посмотрели 100 раз!',
        recipient_list=[email,],
        fail_silently=False,
    )
