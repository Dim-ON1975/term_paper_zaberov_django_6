from django import forms
from .models import Mailing, Message


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('creator', 'mailing_time', 'mailing_frequency',)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
