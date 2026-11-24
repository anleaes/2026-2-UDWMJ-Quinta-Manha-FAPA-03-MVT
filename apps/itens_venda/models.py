from django.db import models

class ItemVenda(models.Model):
    venda = models.ForeignKey(
        'vendas.Venda',
        on_delete=models.CASCADE,
        related_name='itens'
    )

    material = models.ForeignKey(
        'materiais_papelaria.MaterialPapelaria',
        on_delete=models.PROTECT,
        related_name='itens_venda'
    )