from django.views.generic import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect

from logs.models import Logs

CLIENT_LIST = 'logs:logs_list'


class DataMixin:
    paginate_by = 5


class RedirectPermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = None
    login_url = reverse_lazy('clients:error403')

    def handle_no_permission(self):
        return redirect(self.get_login_url())


class LogsListView(RedirectPermissionRequiredMixin, LoginRequiredMixin, DataMixin, ListView):
    model = Logs
    permission_required = 'logs.view_logs'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser:
            queryset = queryset.order_by("-mailing_started", "-status_attempt",).distinct()
        else:
            queryset = queryset.order_by("-mailing_started", "-status_attempt",).filter(
                recipient__creator_id=self.request.user.id).distinct()
            print(self.request.user.id)
        return queryset

