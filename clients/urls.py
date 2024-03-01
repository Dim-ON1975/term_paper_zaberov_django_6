from django.urls import path

from clients.apps import ClientsConfig
from clients.views import ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, HomeView, Error403View

app_name = ClientsConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('error/', Error403View.as_view(), name='error403'),
    path('list/', ClientListView.as_view(), name='client_list'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
]