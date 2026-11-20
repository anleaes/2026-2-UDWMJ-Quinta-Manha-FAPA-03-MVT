from django.urls import path
from . import views

app_name = 'marcas'

urlpatterns = [
    path('listar/', views.listar_marcas, name='listar_marcas'),
    path('adicionar/', views.adicionar_marca, name='adicionar_marca'),
    path('editar/<int:id_marca>/', views.editar_marca, name='editar_marca'),
    path('excluir/<int:id_marca>/', views.excluir_marca, name='excluir_marca'),
]