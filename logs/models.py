from django.db import models

from account.models import NULLABLE


class Logs(models.Model):
    recipient = models.ForeignKey('mailings.Recipient', on_delete=models.CASCADE, verbose_name='рассылка')
    mailing_started = models.DateTimeField(auto_now=True, verbose_name='дата и время попытки')
    status_attempt = models.PositiveIntegerField(verbose_name='статус попытки')
    server_response = models.CharField(max_length=255, **NULLABLE, verbose_name='ответ почтового сервера')

    def __str__(self):
        return f'{self.mailing_started}: {self.status_attempt}, {self.server_response}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
