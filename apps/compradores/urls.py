from django.urls import path
from . import views

app_name = 'compradores'

urlpatterns = [
    path('', views.listar_compradores, name='inicio_compradores'),
    path('listar/', views.listar_compradores, name='listar_compradores'),
    path('cadastrar/', views.adicionar_comprador, name='adicionar_comprador'),
    path('editar-cadastro/<int:id_comprador>/', views.editar_comprador, name='editar_cadastro_comprador'),
    path('excluir/<int:id_comprador>/', views.excluir_comprador, name='excluir_comprador'),
]
