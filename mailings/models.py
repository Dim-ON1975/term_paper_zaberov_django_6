from django.db import models
import datetime

from clients.models import NULLABLE

MODEL_USER = 'account.User'


class Mailing(models.Model):
    @staticmethod
    def str_time(upper_range: int) -> tuple:
        time_choices = []
        for hms in range(0, upper_range):
            hms = str(hms)
            if len(hms) == 1:
                hms = '0' + str(hms)
            hms = tuple((hms, hms))
            time_choices.append(hms)
        time_choices = tuple(time_choices)
        return time_choices

    DAY_CHOICES = []
    for d in range(0, 32):
        if d == 0:
            day = tuple((d, 'от даты создания'))
        else:
            day = tuple((d, str(d)))
        DAY_CHOICES.append(day)
    DAY_CHOICES = tuple(DAY_CHOICES)

    FREQUENCY_CHOICES = (
        (0, 'не повторять'),
        (1, 'один раз в день'),
        (7, 'один раз в неделю'),
        (28, 'один раз в месяц'),
    )

    STATUS_CHOICES = (
        ('завершена', 'завершена'),
        ('создана', 'создана'),
        ('запущена', 'запущена'),
    )

    creator = models.ForeignKey(MODEL_USER, on_delete=models.CASCADE, verbose_name='владелец')
    mailing_hour = models.CharField(default='00', max_length=2, choices=str_time(24), verbose_name='часы')
    mailing_minute = models.CharField(default='00', max_length=2, choices=str_time(60), verbose_name='минуты')
    mailing_second = models.CharField(default='00', max_length=2, choices=str_time(60), verbose_name='секунды')
    mailing_day = models.PositiveIntegerField(default=0, choices=DAY_CHOICES, **NULLABLE, verbose_name='день рассылки')
    mailing_frequency = models.PositiveIntegerField(choices=FREQUENCY_CHOICES,
                                                    verbose_name='периодичность')
    mailing_status = models.CharField(max_length=9, default='создана', choices=STATUS_CHOICES, verbose_name='статус')

    def natural_key(self):
        """Для сериализации связанных данных"""
        return self.pk, self.mailing_hour, self.mailing_minute, self.mailing_second, self.mailing_day, self.mailing_frequency, self.mailing_status

    def __str__(self):
        return (f'старт: {self.mailing_day}-го, {self.mailing_hour}:{self.mailing_minute}:{self.mailing_second}, '
                f'{self.mailing_frequency} дн.')

    class Meta:
        verbose_name = 'параметр рассылки'
        verbose_name_plural = 'параметры рассылки'


class Message(models.Model):
    creator = models.ForeignKey(MODEL_USER, on_delete=models.CASCADE, verbose_name='владелец')
    mail_title = models.CharField(max_length=255, blank=True, verbose_name='тема письма')
    mail_text = models.TextField(max_length=4000, blank=True, verbose_name='текст письма')

    def natural_key(self):
        """Для сериализации связанных данных"""
        return self.pk, self.mail_title, self.mail_text

    def __str__(self):
        return f'{self.mail_title}'

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'


class Recipient(models.Model):
    creator = models.ForeignKey(MODEL_USER, on_delete=models.CASCADE, verbose_name='владелец')
    recipients = models.ManyToManyField('clients.Client', verbose_name='получатели', related_name='recipient')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='письмо')
    mailings = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='параметры')
    date_at = models.DateTimeField(auto_now_add=True, verbose_name='создана')
    date_update = models.DateTimeField(auto_now=True, verbose_name='изменена')

    def __str__(self):
        return f'{self.creator}, {self.message}, {self.mailings}'

    def display_recipients(self):
        """
        Создаёт строку для получателей. Это необходимо для отображения получателей в Admin.
        """
        return ', '.join([recipients.email for recipients in self.recipients.all()])

    display_recipients.short_description = 'получатели'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
