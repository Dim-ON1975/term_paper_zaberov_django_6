from django.contrib import admin

from logs.models import Logs


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('mailings', 'mailing_started', 'status_attempt', 'server_response')
    list_filter = ('mailings', 'mailing_started', 'status_attempt', 'server_response')
    search_fields = ('mailings', 'mailing_started', 'status_attempt', 'server_response')
