from django.urls import path
from . import views

app_name = 'grupos_materiais'

urlpatterns = [
    path('listar/', views.listar_grupos, name='listar_grupos'),
    path('adicionar/', views.adicionar_grupo, name='adicionar_grupo'),
    path('editar/<int:id_grupo>/', views.editar_grupo, name='editar_grupo'),
    path('excluir/<int:id_grupo>/', views.excluir_grupo, name='excluir_grupo'),
]