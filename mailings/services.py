from datetime import datetime

from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def send_mail():
    print(f'Запущен {datetime.now()}')
