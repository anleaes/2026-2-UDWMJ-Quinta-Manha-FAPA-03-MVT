from django.urls import path
from . import views

app_name = 'entradas_estoque'

urlpatterns = [
    path('adicionar/', views.adicionar_entrada, name='adicionar_entrada'),
]
