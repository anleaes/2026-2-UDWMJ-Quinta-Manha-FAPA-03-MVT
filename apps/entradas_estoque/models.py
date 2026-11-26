from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class EntradaEstoque(models.Model):
    fornecedor = models.ForeignKey(
        'fornecedores.Fornecedor',
        on_delete=models.PROTECT,
        verbose_name='Fornecedor',
    )
    material = models.ForeignKey(
        'materiais_papelaria.MaterialPapelaria',
        on_delete=models.PROTECT,
        verbose_name='Material',
    )
    funcionario = models.ForeignKey(
        'funcionarios.Funcionario',
        on_delete=models.PROTECT,
        verbose_name='Funcionário',
    )
    quantidade = models.PositiveIntegerField(
        'Quantidade',
        validators=[MinValueValidator(1)],
    )
    custo_unitario = models.DecimalField(
        'Custo Unitário',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    data_entrada = models.DateTimeField('Data da Entrada', auto_now_add=True)

    class Meta:
        verbose_name = 'Entrada de Estoque'
        verbose_name_plural = 'Entradas de Estoque'
        ordering = ['-data_entrada']

    def __str__(self):
        return f'{self.material} - {self.quantidade} unidades'
