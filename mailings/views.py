# from django.shortcuts import render
# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy, reverse
# from mailings.models import Mailings
#
#
# class DataMixin:
#     paginate_by = 3
#
#
# class MailingsListView(DataMixin, ListView):
#     model = Mailings
#
#
# class MailingsCreateView(CreateView):
#     model = Mailings
#     fields = '__all__'
#     success_url = reverse_lazy('mailings:mailing_list')
#
#
# class MailingsUpdateView(UpdateView):
#     """ Редактирование """
#     model = Mailings
#     fields = '__all__'
#     success_url = reverse_lazy('mailings:mailing_list')
#
#
# class MailingsDeleteView(DeleteView):
#     model = Mailings
#     success_url = reverse_lazy('mailings:mailing_list')
#
