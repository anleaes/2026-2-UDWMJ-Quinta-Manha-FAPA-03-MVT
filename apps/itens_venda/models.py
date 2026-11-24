from django.db import models
from django.core.validators import MinValueValidator


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

    quantidade = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    def calcular_subtotal(self):
        return self.quantidade * self.preco_unitario