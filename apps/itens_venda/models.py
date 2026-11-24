from django.db import models

class ItemVenda(models.Model):
    venda = models.ForeignKey(
        'vendas.Venda',
        on_delete=models.CASCADE,
        related_name='itens'
    )