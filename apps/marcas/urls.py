from django.urls import path
from . import views

app_name = 'marcas'

urlpatterns = [
    path('listar/', views.listar_marca, name='listar_marca'),
]