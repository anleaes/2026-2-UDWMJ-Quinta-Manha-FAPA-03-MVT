from django.contrib import admin
from .models import Estoque


@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'material', 'quantidade', 'estoque_minimo', 'localizacao', 'ultima_atualizacao')
    list_select_related = ('material',)