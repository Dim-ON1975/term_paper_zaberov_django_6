from django.contrib import admin

from mailings.models import Mailing, Message, Recipient


@admin.register(Mailing)
class MailingsAdmin(admin.ModelAdmin):
    list_display = ('creator', 'mailing_hour', 'mailing_minute', 'mailing_second', 'mailing_day', 'mailing_frequency',
                    'mailing_status',)
    list_filter = ('creator', 'mailing_hour', 'mailing_minute', 'mailing_frequency',
                   'mailing_status',)
    search_fields = ('creator', 'mailing_hour', 'mailing_day', 'mailing_frequency',
                     'mailing_status',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('creator', 'mail_title', 'mail_text',)
    list_filter = ('creator', 'mail_title',)
    search_fields = ('creator', 'mail_title', 'mail_text',)


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('creator', 'display_recipients', 'message', 'mailings', 'date_at', 'date_update',)
    list_filter = ('creator', 'recipients', 'message', 'mailings', 'date_at', 'date_update',)
    search_fields = ('creator', 'recipients', 'message', 'mailings')
