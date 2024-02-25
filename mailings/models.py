from django.db import models
import datetime

from clients.models import NULLABLE

MODEL_USER = 'account.User'


class Mailing(models.Model):
    TIME_CHOICES = []
    for h in range(0, 24):
        time = tuple((datetime.time(h, 00, 00), datetime.time(h, 00, 00)))
        TIME_CHOICES.append(time)
    TIME_CHOICES = tuple(TIME_CHOICES)

    FREQUENCY_CHOICES = (
        (0, 'не повторять'),
        (1, 'один раз в день'),
        (7, 'один раз в неделю'),
        (28, 'один раз в месяц'),
    )

    STATUS_CHOICES = (
        (0, ''),
        (1, 'завершена'),
        (2, 'создана'),
        (3, 'запущена'),
    )

    creator = models.ForeignKey(MODEL_USER, on_delete=models.CASCADE, verbose_name='владелец')
    mailing_time = models.TimeField(auto_now=False, auto_now_add=False, choices=TIME_CHOICES,
                                    verbose_name='время рассылки')
    mailing_frequency = models.PositiveIntegerField(choices=FREQUENCY_CHOICES,
                                                    verbose_name='периодичность')
    mailing_status = models.CharField(max_length=9, default='', choices=STATUS_CHOICES, verbose_name='статус')

    def __str__(self):
        return f'{self.creator} ({self.mailing_time}, периодичность: {self.mailing_frequency} дн.)'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Message(models.Model):
    creator = models.ForeignKey(MODEL_USER, on_delete=models.CASCADE, verbose_name='владелец')
    mail_title = models.CharField(max_length=255, blank=True, verbose_name='тема письма')
    mail_text = models.TextField(max_length=4000, blank=True, verbose_name='текст письма')

    def __str__(self):
        return f'{self.mail_title}: {self.mail_text}'

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'


class Recipient(models.Model):
    creator = models.ForeignKey(MODEL_USER, on_delete=models.CASCADE, verbose_name='владелец')
    recipients = models.ManyToManyField('clients.Client', verbose_name='получатель')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='владелец')
    mailings = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')

    class Meta:
        verbose_name = 'получатель'
        verbose_name_plural = 'получатели'
