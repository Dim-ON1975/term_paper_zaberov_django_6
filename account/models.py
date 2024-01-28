from django.db import models
from django.conf import settings

NULLABLE = {'blank': True, 'null': True}


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    date_of_birth = models.DateField(**NULLABLE, verbose_name='дата рождения')
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', **NULLABLE, verbose_name='фотография')

    def __str__(self):
        return f'Профиль {self.user.username}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
