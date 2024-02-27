from django.contrib import admin

from logs.models import Logs


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'mailing_started', 'status_attempt', 'server_response')
    list_filter = ('recipient', 'mailing_started', 'status_attempt', 'server_response')
    search_fields = ('recipient', 'mailing_started', 'status_attempt', 'server_response')
