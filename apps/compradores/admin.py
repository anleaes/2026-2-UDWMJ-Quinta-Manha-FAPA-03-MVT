
from django.contrib import admin
from .models import Comprador


@admin.register(Comprador)
class CompradorAdmin(admin.ModelAdmin):
    list_display = (
        'nome_completo',
        'cpf',
        'telefone_contato',
        'data_nascimento',
        'data_cadastro',
    )

    search_fields = (
        'nome_completo',
        'cpf',
    )

    ordering = ('nome_completo',)
