from django.contrib import admin

from mailings.models import Mailing, Message, Recipient


@admin.register(Mailing)
class MailingsAdmin(admin.ModelAdmin):
    list_display = ('creator', 'mailing_hour', 'mailing_minute', 'mailing_second', 'mailing_day', 'mailing_frequency',)
    list_filter = ('creator', 'mailing_hour', 'mailing_minute', 'mailing_frequency',)
    search_fields = ('creator', 'mailing_hour', 'mailing_day', 'mailing_frequency',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('creator', 'mail_title', 'mail_text',)
    list_filter = ('creator', 'mail_title',)
    search_fields = ('creator', 'mail_title', 'mail_text',)


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('creator', 'mailing_status', 'is_active', 'display_recipients', 'message', 'mailings', 'date_at',
                    'date_update', 'date_start', 'mailings_count',)
    list_filter = ('creator', 'mailing_status', 'is_active', 'recipients', 'message', 'mailings',
                   'date_at', 'date_update', 'mailings_count',)
    search_fields = ('creator', 'mailing_status', 'recipients', 'message', 'mailings',)
