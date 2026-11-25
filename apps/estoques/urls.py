from django.urls import path
from . import views

app_name = 'estoques'

urlpatterns = [
    path('listar/', views.listar_estoques, name='listar_estoques'),
]