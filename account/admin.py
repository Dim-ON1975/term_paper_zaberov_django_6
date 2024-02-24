from django.contrib import admin
from account.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser',
        'email_verify',)
    list_filter = ('email', 'email_verify', 'is_staff', 'is_active', 'is_superuser',)
    search_fields = ('first_name', 'last_name', 'email',)
