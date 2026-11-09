from django.urls import path
from . import views

app_name = 'grupos_materiais'

urlpatterns = [
    path('listar/', views.listar_grupos, name='listar_grupos'),
]