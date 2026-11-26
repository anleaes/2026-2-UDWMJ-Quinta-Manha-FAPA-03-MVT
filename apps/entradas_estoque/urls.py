from django.urls import path
from . import views

app_name = 'entradas_estoque'

urlpatterns = [
    path('adicionar/', views.adicionar_entrada, name='adicionar_entrada'),
    path('listar/', views.listar_entradas, name='listar_entradas'),
    path(
        'consultar/<int:id_entrada>/',
        views.consultar_entrada,
        name='consultar_entrada',
    ),
]
