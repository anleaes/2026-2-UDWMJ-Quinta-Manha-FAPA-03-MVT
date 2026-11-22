from django.urls import path

from . import views

app_name = 'materiais_papelaria'

urlpatterns = [
    path('listar/', views.listar_materiais, name='listar_materiais'),
    path('adicionar/', views.adicionar_material, name='adicionar_material'),
    path('editar/<int:id_material>/', views.editar_material, name='editar_material'),
    path('excluir/<int:id_material>/', views.excluir_material, name='excluir_material'),
]
