from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy, reverse
from clients.models import Client
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404


CLIENT_LIST = 'clients:client_list'


class DataMixin:
    paginate_by = 5


class RedirectPermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = None
    login_url = reverse_lazy('clients:error403')

    def handle_no_permission(self):
        return redirect(self.get_login_url())


class ClientListView(RedirectPermissionRequiredMixin, LoginRequiredMixin, DataMixin, ListView):
    model = Client
    permission_required = 'clients.view_client'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser:
            queryset = queryset.order_by("last_name", "first_name", "middle_name", ).distinct()
        else:
            queryset = queryset.order_by("last_name", "first_name", "middle_name", ).filter(
                creator=self.request.user).distinct()
        return queryset


class ClientCreateView(RedirectPermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Client
    fields = '__all__'
    permission_required = 'clients.add_client'
    success_url = reverse_lazy(CLIENT_LIST)

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


class ClientUpdateView(RedirectPermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """ Редактирование товара """
    model = Client
    fields = '__all__'
    permission_required = 'clients.change_client'
    success_url = reverse_lazy(CLIENT_LIST)

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


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy(CLIENT_LIST)

    def test_func(self):
        client = self.get_object()
        return self.request.user == client.creator or self.request.user.is_superuser


class HomeView(TemplateView):
    template_name = 'clients/home.html'


class Error403View(TemplateView):
    template_name = 'clients/error_403.html'
