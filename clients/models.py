from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    last_name = models.CharField(max_length=20, verbose_name='фамилия')
    first_name = models.CharField(max_length=20, verbose_name='имя')
    middle_name = models.CharField(max_length=20, **NULLABLE, verbose_name='отчество')
    email = models.EmailField(verbose_name='электронная почта')
    comment = models.CharField(max_length=200, **NULLABLE, verbose_name='комментарий')

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

# class Recipient(models.Model):
#     creator = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='владелец')
#     recipients = models.ManyToManyField(Client, verbose_name='получатель')
#
#     class Meta:
#         verbose_name = 'получатель'
#         verbose_name_plural = 'получатели'
#
#
# class Message(models.Model):
#     creator = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='владелец')
#
#
# class Logs(models.Model):
#     mailings = models.ForeignKey(Mailings, on_delete=models.CASCADE, verbose_name='рассылка')
