from django.contrib import admin

from clients.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'email', 'comment',)
    list_filter = ('last_name', 'first_name', 'middle_name',)
    search_fields = ('last_name', 'first_name', 'middle_name', 'email',)

