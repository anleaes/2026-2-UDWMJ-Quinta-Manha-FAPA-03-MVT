from django.urls import path
from . import views

app_name = 'itens_venda'

urlpatterns = [
    path('<int:id_venda>/cadastrar/', views.adicionar_item, name='adicionar_item'),
]