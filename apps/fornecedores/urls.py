from django.urls import path
from . import views

app_name = 'fornecedores'

urlpatterns = [
    path('listar/', views.listar_fornecedores, name='listar_fornecedores'),
    path('adicionar/', views.adicionar_fornecedor, name='adicionar_fornecedor'),
    path('editar/<int:id_fornecedor>/', views.editar_fornecedor, name='editar_fornecedor'),
]
