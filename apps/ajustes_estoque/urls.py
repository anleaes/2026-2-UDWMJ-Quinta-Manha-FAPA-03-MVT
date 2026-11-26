from django.urls import path

from . import views

app_name = 'ajustes_estoque'

urlpatterns = [
    path('adicionar/', views.adicionar_ajuste, name='adicionar_ajuste'),
    path('listar/', views.listar_ajustes, name='listar_ajustes'),
]
