from django.urls import path
from . import views

app_name = 'estoques'

urlpatterns = [
    path('listar/', views.listar_estoques, name='listar_estoques'),
    path('adicionar/', views.adicionar_estoque, name='adicionar_estoque'),
    path('editar/<int:id_estoque>/', views.editar_estoque, name='editar_estoque'),
]