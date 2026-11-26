from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, transaction
from estoques.models import Estoque


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

    def registrar_entrada(self):
        with transaction.atomic():
            try:
                estoque = Estoque.objects.select_for_update().get(
                    material_id=self.material_id
                )
            except Estoque.DoesNotExist:
                raise ValidationError(
                    'Não existe estoque cadastrado para este material.'
                )

            self.full_clean()
            self.save()
            estoque.adicionar_quantidade(self.quantidade)

    class Meta:
        verbose_name = 'Entrada de Estoque'
        verbose_name_plural = 'Entradas de Estoque'
        ordering = ['-data_entrada']

    def __str__(self):
        return f'{self.material} - {self.quantidade} unidades'
