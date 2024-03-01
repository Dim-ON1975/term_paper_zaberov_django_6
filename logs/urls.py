from django.urls import path

from logs.apps import LogsConfig
from logs.views import LogsListView

app_name = LogsConfig.name

urlpatterns = [
    path('logs/', LogsListView.as_view(), name='logs_list')
]