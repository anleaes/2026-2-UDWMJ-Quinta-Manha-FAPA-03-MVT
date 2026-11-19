from django.urls import path
from . import views

app_name = 'funcionarios'

urlpatterns = [
    path('adicionar/', views.adicionar_funcionario, name='adicionar_funcionario'),
]