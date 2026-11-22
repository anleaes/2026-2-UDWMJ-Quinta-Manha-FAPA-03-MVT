from django.urls import path

from . import views

app_name = 'materiais_papelaria'

urlpatterns = [
    path('listar/', views.listar_materiais, name='listar_materiais'),
]
