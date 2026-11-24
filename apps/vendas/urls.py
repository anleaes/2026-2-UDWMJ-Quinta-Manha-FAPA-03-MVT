from django.urls import path

from . import views

app_name = 'vendas'

urlpatterns = [
    path('cadastrar/', views.adicionar_venda, name='adicionar_venda'),
    path('listar/', views.listar_vendas, name='listar_vendas'),
    path('detalhar/<int:id_venda>/', views.detalhar_venda, name='detalhar_venda'),
    path('editar/<int:id_venda>/', views.editar_venda, name='editar_venda'),
    path('cancelar/<int:id_venda>/', views.cancelar_venda, name='cancelar_venda'),
]