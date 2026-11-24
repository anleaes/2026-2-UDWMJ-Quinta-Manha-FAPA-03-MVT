from django.urls import path
from . import views

app_name = 'itens_venda'

urlpatterns = [
    path('<int:id_venda>/cadastrar/', views.adicionar_item, name='adicionar_item'),
    path('<int:id_venda>/listar/', views.listar_itens, name='listar_itens'),
    path('<int:id_venda>/editar/<int:id_item>/', views.editar_item, name='editar_item'),
    path('<int:id_venda>/remover/<int:id_item>/', views.remover_item, name='remover_item'),
]