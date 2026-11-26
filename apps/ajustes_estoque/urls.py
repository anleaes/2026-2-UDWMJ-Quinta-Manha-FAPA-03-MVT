from django.urls import path

from . import views

app_name = 'ajustes_estoque'

urlpatterns = [
    path('listar/', views.listar_ajustes, name='listar_ajustes'),
]
