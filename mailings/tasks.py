import json
import os

from datetime import datetime

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
    current_datatime = datetime.now().replace(microsecond=0)
    current_date = current_datatime.date()
    current_day_number = current_date.day
    current_time = current_datatime.time()

    # Сериализация рассылок
    serialized_data = serializers.serialize('json', Recipient.objects.all(), use_natural_foreign_keys=True)
    # преобразуем в объект Python
    serialized_data = json.loads(serialized_data)

    # Рассылка сообщений в зависимости от передаваемых параметров
    for mailing in serialized_data:
        print('В цикл зашли')
        str_time = mailing["fields"]['mailings'][1] + ':' + mailing["fields"]['mailings'][2] + ':' + \
                   mailing["fields"]['mailings'][3]
        mailing_time = datetime.strptime(str_time, '%H:%M:%S').time()
        mailing_day = mailing["fields"]['mailings'][4]
        mailing_frequency = mailing["fields"]['mailings'][5]
        mailing_status = mailing["fields"]['mailings'][6]

        # Одноразовая рассылка
        if mailing_frequency == 0 and mailing_status == 'создана':
            if mailing_day == int(current_day_number) and mailing_time == current_time:
                Mailing.objects.filter(id=mailing["fields"]['mailings'][0]).update(mailing_status='запущена')
                send_email(mailing["fields"]['message'][1],
                           mailing["fields"]['message'][2],
                           mailing["fields"]['recipients'],
                           mailing['pk'])
                Mailing.objects.filter(id=mailing["fields"]['mailings'][0]).update(mailing_status='завершена')


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
