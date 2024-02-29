from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from core.settings import LOGIN_URL
from mailings.forms import MailingForm, MessageForm, RecipientForm
from mailings.models import Mailing, Message, Recipient
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.forms import ValidationError
from django.contrib.auth.decorators import login_required, user_passes_test

from datetime import datetime
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404

MAILING_LIST = 'mailings:mailing_list'
MESSAGE_LIST = 'mailings:message_list'
RECIPIENT_LIST = 'mailings:recipient_list'


class RedirectPermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = None
    login_url = reverse_lazy('clients:error403')

    def handle_no_permission(self):
        return redirect(self.get_login_url())


class DataMixin:
    paginate_by = 5


class MailingListView(RedirectPermissionRequiredMixin, LoginRequiredMixin, DataMixin, ListView):
    model = Mailing
    permission_required = 'mailings.view_mailing'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser:
            queryset = queryset.order_by("-mailing_day", "-mailing_hour", "-mailing_minute", "-mailing_second",
                                         "-mailing_frequency").distinct()
        else:
            queryset = queryset.order_by("-mailing_day", "-mailing_hour", "-mailing_minute", "-mailing_second",
                                         "-mailing_frequency").filter(creator=self.request.user).distinct()
        return queryset


class MailingCreateView(RedirectPermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    permission_required = 'mailings.add_mailing'
    success_url = reverse_lazy(MAILING_LIST)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser:
            return self.object
        if not self.request.user.is_staff:
            raise Http404
        return self.object

    def form_valid(self, form):
        # Получаем текущего пользователя
        user = self.request.user
        # Присваиваем текущего пользователя полю user нового продукта
        form.instance.user = user
        # текущие дата и время
        current_datetime = datetime.now().replace(microsecond=0)
        current_date = current_datetime.date()
        current_day_number = current_date.day
        current_month_number = current_date.month
        current_year_number = current_date.year
        mailing_day = form.cleaned_data['mailing_day']
        if mailing_day == 0:
            mailing_day = current_day_number
        try:
            # данные формы
            mailing_hour = form.cleaned_data['mailing_hour']
            mailing_minute = form.cleaned_data['mailing_minute']
            mailing_second = form.cleaned_data['mailing_second']
            date_time_str = str((f'{current_year_number}-{current_month_number}-{mailing_day} '
                                 f'{mailing_hour}:{mailing_minute}:{mailing_second}'))
            mailing_datetime = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

            if mailing_datetime < current_datetime:
                form.add_error('mailing_day', ValidationError('Выбранные дата и время не могут быть меньше текущих.'))
                return super().form_invalid(form)
        except:
            form.add_error('mailing_day', ValidationError('Возможно такого дня в текущем месяце нет.'))
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_form_kwargs(self):
        # Получаем ключевые аргументы для формы
        kwargs = super().get_form_kwargs()
        # Изменяем аргументы формы, добавляя пользователя в их начальные значения
        kwargs['initial'] = {'creator': self.request.user}
        return kwargs


class MailingUpdateView(RedirectPermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """ Редактирование """
    model = Mailing
    form_class = MailingForm
    permission_required = 'mailings.change_mailing'
    success_url = reverse_lazy(MAILING_LIST)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.groups.filter(name='manager').exists() or self.request.user.groups.filter(
                name='reg_user').exists() or self.request.user.is_superuser:
            return self.object
        if not self.request.user.is_staff:
            raise Http404
        return self.object

    def form_valid(self, form):
        # Получаем текущего пользователя
        user = self.request.user
        # Присваиваем текущего пользователя полю user нового продукта
        form.instance.user = user
        # текущие дата и время
        current_datetime = datetime.now().replace(microsecond=0)
        current_date = current_datetime.date()
        current_day_number = current_date.day
        current_month_number = current_date.month
        current_year_number = current_date.year
        mailing_day = form.cleaned_data['mailing_day']
        if mailing_day == 0:
            mailing_day = current_day_number
        try:
            # данные формы
            mailing_hour = form.cleaned_data['mailing_hour']
            mailing_minute = form.cleaned_data['mailing_minute']
            mailing_second = form.cleaned_data['mailing_second']
            date_time_str = str((f'{current_year_number}-{current_month_number}-{mailing_day} '
                                 f'{mailing_hour}:{mailing_minute}:{mailing_second}'))
            mailing_datetime = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

            if mailing_datetime < current_datetime:
                form.add_error('mailing_day', ValidationError('Выбранные дата и время не могут быть меньше текущих.'))
                return super().form_invalid(form)
        except:
            form.add_error('mailing_day', ValidationError('Возможно такого дня в текущем месяце нет.'))
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_form_kwargs(self):
        # Получаем ключевые аргументы для формы
        kwargs = super().get_form_kwargs()
        # Изменяем аргументы формы, добавляя пользователя в их начальные значения
        kwargs['initial'] = {'creator': self.request.user}
        return kwargs


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy(MAILING_LIST)

    def test_func(self):
        mailing = self.get_object()
        return self.request.user == mailing.creator or self.request.user.is_superuser


class MessageListView(LoginRequiredMixin, DataMixin, ListView):
    model = Message

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser:
            queryset = queryset.order_by("-creator", "-mail_title").distinct()
        else:
            queryset = queryset.order_by("-mail_title").filter(creator=self.request.user).distinct()
        return queryset


class MessageDetailView(RedirectPermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = Message
    permission_required = 'mailings.view_message'


class MessageCreateView(RedirectPermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    permission_required = 'mailings.add_message'
    success_url = reverse_lazy(MESSAGE_LIST)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser:
            return self.object
        if not self.request.user.is_staff:
            raise Http404
        return self.object

    def form_valid(self, form):
        # Получаем текущего пользователя
        user = self.request.user
        # Присваиваем текущего пользователя полю user нового продукта
        form.instance.user = user
        # Сохраняем экземпляр модели перед вызовом super().form_valid()
        return super().form_valid(form)

    def get_form_kwargs(self):
        # Получаем ключевые аргументы для формы
        kwargs = super().get_form_kwargs()
        # Изменяем аргументы формы, добавляя пользователя в их начальные значения
        kwargs['initial'] = {'creator': self.request.user}
        return kwargs


class MessageUpdateView(RedirectPermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """ Редактирование """
    model = Message
    form_class = MessageForm
    permission_required = 'mailings.change_message'
    success_url = reverse_lazy(MESSAGE_LIST)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.groups.filter(name='manager').exists() or self.request.user.groups.filter(
                name='reg_user').exists() or self.request.user.is_superuser:
            return self.object
        if not self.request.user.is_staff:
            raise Http404
        return self.object

    def form_valid(self, form):
        # Получаем текущего пользователя
        user = self.request.user
        # Присваиваем текущего пользователя полю user нового продукта
        form.instance.user = user
        # Сохраняем экземпляр модели перед вызовом super().form_valid()
        return super().form_valid(form)

    def get_form_kwargs(self):
        # Получаем ключевые аргументы для формы
        kwargs = super().get_form_kwargs()
        # Изменяем аргументы формы, добавляя пользователя в их начальные значения
        kwargs['initial'] = {'creator': self.request.user}
        return kwargs


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy(MESSAGE_LIST)

    def test_func(self):
        message = self.get_object()
        return self.request.user == message.creator or self.request.user.is_superuser


class RecipientListView(RedirectPermissionRequiredMixin, LoginRequiredMixin, DataMixin, ListView):
    model = Recipient
    permission_required = 'mailings.view_recipient'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser:
            queryset = queryset.order_by("-is_active", "-date_start").distinct()
        else:
            queryset = queryset.order_by("-is_active", "-date_start").filter(creator=self.request.user).distinct()
        return queryset


class RecipientDetailView(RedirectPermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = Recipient
    permission_required = 'mailings.view_recipient'


class RecipientCreateView(RedirectPermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    permission_required = 'mailings.add_recipient'
    success_url = reverse_lazy(RECIPIENT_LIST)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.groups.filter(name='manager').exists() or self.request.user.groups.filter(
                name='reg_user').exists() or self.request.user.is_superuser:
            return self.object
        if not self.request.user.is_staff:
            raise Http404
        return self.object

    def form_valid(self, form):
        # Получаем текущего пользователя
        user = self.request.user
        # Присваиваем текущего пользователя полю user нового продукта
        form.instance.user = user
        # Сохраняем экземпляр модели перед вызовом super().form_valid()
        return super().form_valid(form)

    def get_form_kwargs(self):
        # Получаем ключевые аргументы для формы
        kwargs = super().get_form_kwargs()
        # Изменяем аргументы формы, добавляя пользователя в их начальные значения
        kwargs['initial'] = {'creator': self.request.user}
        return kwargs


class RecipientUpdateView(RedirectPermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """ Редактирование """
    model = Recipient
    form_class = RecipientForm
    permission_required = 'mailings.change_recipient'
    success_url = reverse_lazy(RECIPIENT_LIST)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.groups.filter(name='manager').exists() or self.request.user.groups.filter(
                name='reg_user').exists() or self.request.user.is_superuser:
            return self.object
        if not self.request.user.is_staff:
            raise Http404
        return self.object

    def form_valid(self, form):
        # Получаем текущего пользователя
        user = self.request.user
        # Присваиваем текущего пользователя полю user нового продукта
        form.instance.user = user
        # Сохраняем экземпляр модели перед вызовом super().form_valid()
        return super().form_valid(form)

    def get_form_kwargs(self):
        # Получаем ключевые аргументы для формы
        kwargs = super().get_form_kwargs()
        # Изменяем аргументы формы, добавляя пользователя в их начальные значения
        kwargs['initial'] = {'creator': self.request.user}
        return kwargs


class RecipientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy(RECIPIENT_LIST)

    def test_func(self):
        recipient = self.get_object()
        return self.request.user == recipient.creator or self.request.user.is_superuser


@login_required
@user_passes_test(lambda u: lambda recipient_id: u == get_object_or_404(Recipient, pk=recipient_id).user,
                  login_url=LOGIN_URL)
def toggle_activity(request, pk):
    """ Активация/деактивация рассылки """
    recipient_item = get_object_or_404(Recipient, pk=pk)
    if recipient_item.is_active:
        recipient_item.is_active = False
        recipient_item.mailing_status = 'завершена'
    else:
        recipient_item.is_active = True
        recipient_item.mailing_status = 'запущена'

    recipient_item.save()

    return redirect(reverse('mailings:recipient_list'))
