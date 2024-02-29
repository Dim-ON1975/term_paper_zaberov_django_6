from django.urls import path

from mailings.apps import MailingConfig
from mailings.views import MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, MessageListView, \
    MessageCreateView, MessageUpdateView, MessageDeleteView, MessageDetailView, RecipientListView, \
    RecipientCreateView, RecipientUpdateView, RecipientDeleteView, RecipientDetailView, toggle_activity

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
    # получатели
    path('recipient-list/', RecipientListView.as_view(), name='recipient_list'),
    path('recipient-detail/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipient-create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipient-update/<int:pk>/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient-delete/<int:pk>/', RecipientDeleteView.as_view(), name='recipient_delete'),
    # активация/деактивация товара
    path('activity/<int:pk>', toggle_activity, name='activity')
]
