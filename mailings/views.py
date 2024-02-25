from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from mailings.forms import MailingForm, MessageForm
from mailings.models import Mailing, Message
from django.contrib.auth.mixins import LoginRequiredMixin

MAILING_LIST = 'mailings:mailing_list'
MESSAGE_LIST = 'mailings:message_list'


class DataMixin:
    paginate_by = 5


class MailingListView(LoginRequiredMixin, DataMixin, ListView):
    model = Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy(MAILING_LIST)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """ Редактирование """
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy(MAILING_LIST)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy(MAILING_LIST)


class MessageListView(LoginRequiredMixin, DataMixin, ListView):
    model = Message


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy(MESSAGE_LIST)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """ Редактирование """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy(MESSAGE_LIST)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy(MESSAGE_LIST)
