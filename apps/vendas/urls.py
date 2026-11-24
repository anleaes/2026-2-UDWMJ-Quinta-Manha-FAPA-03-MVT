from django.urls import path

from . import views

app_name = 'vendas'

urlpatterns = [
    path('cadastrar/', views.adicionar_venda, name='adicionar_venda'),
]