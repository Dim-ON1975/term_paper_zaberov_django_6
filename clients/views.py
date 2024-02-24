from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy, reverse
from clients.models import Client


class DataMixin:
    paginate_by = 3


class ClientListView(DataMixin, ListView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('clients:client_list')


class ClientUpdateView(UpdateView):
    """ Редактирование товара """
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('clients:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('clients:client_list')


class HomeView(TemplateView):
    template_name = 'clients/home.html'