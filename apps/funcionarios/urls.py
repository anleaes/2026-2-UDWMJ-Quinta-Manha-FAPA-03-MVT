from django.urls import path
from . import views

app_name = 'funcionarios'

urlpatterns = [
    path('adicionar/', views.adicionar_funcionario, name='adicionar_funcionario'),
    path('listar/', views.listar_funcionarios, name='listar_funcionarios'),
    path('editar/<int:id_funcionario>/', views.editar_funcionario, name='editar_funcionario'),
    path('excluir/<int:id_funcionario>/', views.excluir_funcionario, name='excluir_funcionario'),
]