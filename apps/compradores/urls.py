
from django.urls import path
from . import views

app_name = 'compradores'

urlpatterns = [
    path('listar/', views.listar_compradores, name='listar_compradores'),
    path('adicionar/', views.adicionar_comprador, name='adicionar_comprador'),
    path('editar/<int:id_comprador>/', views.editar_comprador, name='editar_comprador'),
    path('excluir/<int:id_comprador>/', views.excluir_comprador, name='excluir_comprador'),
]
