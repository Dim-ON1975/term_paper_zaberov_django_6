from django import forms
from .models import Mailing, Message, Recipient


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('creator', 'mailing_hour', 'mailing_minute', 'mailing_second', 'mailing_day', 'mailing_frequency',)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ('creator', 'recipients', 'message', 'mailings')
