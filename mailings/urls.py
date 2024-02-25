from django.urls import path

from mailings.apps import MailingConfig
from mailings.views import MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, MessageListView, \
    MessageCreateView, MessageUpdateView, MessageDeleteView, MessageDetailView

app_name = MailingConfig.name

urlpatterns = [
    # рассылки
    path('mailing-list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing-create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing-update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing-delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    # сообщения
    path('message-list/', MessageListView.as_view(), name='message_list'),
    path('message-detail/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message-create/', MessageCreateView.as_view(), name='message_create'),
    path('message-update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message-delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
]
