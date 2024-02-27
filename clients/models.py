from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    last_name = models.CharField(max_length=20, verbose_name='фамилия')
    first_name = models.CharField(max_length=20, verbose_name='имя')
    middle_name = models.CharField(max_length=20, **NULLABLE, verbose_name='отчество')
    email = models.EmailField(verbose_name='электронная почта')
    comment = models.CharField(max_length=200, **NULLABLE, verbose_name='комментарий')

    def natural_key(self):
        """Для сериализации связанных данных"""
        return self.email

    def __str__(self):
        if self.middle_name:
            full_name = f'{str(self.last_name)} {str(self.first_name)} {str(self.middle_name)[0]}.'.title()
        else:
            full_name = f'{str(self.last_name)} {str(self.first_name)}'.title()

        return f'{full_name} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ('last_name', 'first_name',)
