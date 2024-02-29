import json
import os

from datetime import datetime
from calendar import monthrange

from core.celery import app
from dotenv import load_dotenv, find_dotenv
from django.core.mail import send_mail, BadHeaderError

from logs.models import Logs
from mailings.models import Recipient, Mailing
from django.core import serializers

# переменные окружения в файле .env
load_dotenv(find_dotenv())


@app.task
def send_process(*args, **kwargs):
    # Текущие дата и время
    current_datetime = datetime.now().replace(microsecond=0)
    current_date = current_datetime.date()
    current_day_number = current_date.day
    current_time = current_datetime.time()
    # Количество дней в текущем месяце
    current_year = datetime.now().year
    current_month_number = current_date.month
    days = monthrange(current_year, current_month_number)[1]

    # Сериализация рассылок
    serialized_data = serializers.serialize('json',
                                            Recipient.objects.all().exclude(mailing_status='завершена'),
                                            use_natural_foreign_keys=True)
    # преобразуем в объект Python
    serialized_data = json.loads(serialized_data)


    # Рассылка сообщений
    for mailing in serialized_data:
        str_time = mailing["fields"]['mailings'][1] + ':' + mailing["fields"]['mailings'][2] + ':' + \
                   mailing["fields"]['mailings'][3]
        mailing_time = datetime.strptime(str_time, '%H:%M:%S').time()
        mailing_day = mailing["fields"]['mailings'][4]
        mailing_frequency = mailing["fields"]['mailings'][5]
        # Определяем дату на конец текущего месяца для ежемесячной отправки,
        # если дата, выбранная пользователем, больше, чем количество дней в текущем месяце.
        if mailing_frequency == 28 and days < mailing_day:
            mailing_day = days
        # Определим дату при условии, что выбран вариант рассылки "от даты создания"
        if mailing_day == 0:
            date_at = mailing["fields"]['date_at'][:10]
            mailing_day = datetime.strptime(date_at, '%Y-%m-%d').day
        mailing_status = mailing["fields"]['mailing_status']
        mailings_count = mailing["fields"]['mailings_count']

        # Одноразовая рассылка
        if mailing_frequency == 0 and mailing_status == 'создана':
            if mailing_day == int(current_day_number) and mailing_time == current_time:
                Recipient.objects.filter(id=mailing["pk"]).update(mailing_status='запущена')
                # Фиксируем дату рассылки
                if mailing["fields"]['date_start'] is None:
                    Recipient.objects.filter(id=mailing["pk"]).update(date_start=current_date)
                # Рассылка
                send_email(mailing["fields"]['message'][1],
                           mailing["fields"]['message'][2],
                           mailing["fields"]['recipients'],
                           mailing['pk'])
                # Количество рассылок
                Recipient.objects.filter(id=mailing["pk"]).update(mailings_count=mailings_count + 1,
                                                                  mailing_status='завершена', is_active=False)

        # Периодическая рассылка
        if mailing_frequency > 0 and mailing_status != 'завершена':
            if mailing_day == int(current_day_number) and mailing_time == current_time:
                Recipient.objects.filter(id=mailing["pk"]).update(mailing_status='запущена')
                # Фиксируем дату начала рассылок
                if mailing["fields"]['date_start'] is None:
                    Recipient.objects.filter(id=mailing["pk"]).update(date_start=current_date)
                # Рассылка
                send_email(mailing["fields"]['message'][1],
                           mailing["fields"]['message'][2],
                           mailing["fields"]['recipients'],
                           mailing['pk'])
                if mailing_frequency != 28:
                    # Проверяем границу окончания месяца
                    days_end_of_month = days - current_day_number  # дней до конца месяца
                    remainder_of_period = days_end_of_month - mailing_frequency  # остаток периода
                    if days_end_of_month == 0:
                        mailing_day = 0
                    elif remainder_of_period < 0:
                        mailing_day = 0
                        mailing_frequency = abs(remainder_of_period)
                    # Увеличиваем дату на частоту повторов
                    Mailing.objects.filter(id=mailing["fields"]['mailings'][0]).update(
                        mailing_day=mailing_day + mailing_frequency)
                # Количество рассылок
                Recipient.objects.filter(id=mailing["pk"]).update(mailings_count=mailings_count + 1)


def send_email(subject: str, message: str, recipient_list: list, recipient_id: int):
    """
    Отправка сообщения по электронной почте.
    :param subject: Тема письма, str.
    :param message: Текст письма, str.
    :param recipient_list: Список адресов электронной почты, list.
    :param recipient_id: ID рассылки, int.
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=os.getenv('DEFAULT_FROM_EMAIL_YANDEX'),
            recipient_list=recipient_list,
            fail_silently=False,
        )
        Logs.objects.create(recipient_id=recipient_id, status_attempt=200, server_response='OK')
    except BadHeaderError as err:
        Logs.objects.create(recipient_id=recipient_id, status_attempt=500, server_response=str(err))
    except ValueError as err:
        Logs.objects.create(recipient_id=recipient_id, status_attempt=400, server_response=str(err))
