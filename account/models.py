from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='электронная почта')
    email_verify = models.BooleanField(default=False, verbose_name='верификация почты')
    date_of_birth = models.DateField(**NULLABLE, verbose_name='дата рождения')
    avatar = models.ImageField(upload_to='users/%Y/%m/%d/', **NULLABLE, verbose_name='аватар')
    phone = models.CharField(max_length=35, **NULLABLE, verbose_name='телефон')
    country = models.CharField(max_length=100, verbose_name='страна', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
