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
        if not self._state.adding or (
            self.pk is not None and self.__class__.objects.filter(pk=self.pk).exists()
        ):
            raise ValidationError('Esta entrada já foi registrada.')

        if any(value is None for value in (
            self.fornecedor_id,
            self.material_id,
            self.funcionario_id,
        )):
            raise ValidationError(
                'Selecione um fornecedor, um material e um funcionário cadastrados.'
            )

        if type(self.quantidade) is not int or self.quantidade <= 0:
            raise ValidationError(
                'Informe uma quantidade inteira maior que zero.'
            )

        if (
            not isinstance(self.custo_unitario, Decimal)
            or not self.custo_unitario.is_finite()
        ):
            raise ValidationError('Informe um custo unitário válido.')

        if self.custo_unitario < 0:
            raise ValidationError('O custo unitário não pode ser negativo.')

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
