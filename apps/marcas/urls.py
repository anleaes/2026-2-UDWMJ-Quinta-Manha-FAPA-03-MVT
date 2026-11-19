from django.urls import path
from . import views

app_name = 'marcas'

urlpatterns = [
    path('listar/', views.listar_marca, name='listar_marca'),
    path('adicionar/', views.adicionar_marca, name='adicionar_marca'),
]
