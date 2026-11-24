from django.db import models, transaction
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


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

    def _validar_venda_aberta(self):
        if self.venda.status != self.venda.Status.ABERTA:
            raise ValidationError(
                "Somente vendas abertas podem ter seus itens alterados."
            )

    def _validar_material_ativo(self):
        if not self.material.ativo:
            raise ValidationError(
                "O material precisa estar ativo."
            )

    def _atualizar_total_venda(self):
        self.venda.valor_total = self.venda.calcular_total()
        self.venda.save(update_fields=["valor_total"])

    @transaction.atomic
    def adicionar_item(self):
        if self.pk is not None:
            raise ValidationError(
                "Este item ja esta cadastrado."
            )

        self._validar_venda_aberta()
        self._validar_material_ativo()

        self.preco_unitario = self.material.preco_venda

        self.full_clean()
        self.save()

        self._atualizar_total_venda()

    @transaction.atomic
    def atualizar_dados(self, quantidade):
        if self.pk is None:
            raise ValidationError(
                "O item precisa estar cadastrado."
            )

        self._validar_venda_aberta()

        self.quantidade = quantidade

        self.full_clean()
        self.save(update_fields=["quantidade"])

        self._atualizar_total_venda()

    @transaction.atomic
    def remover_item(self):
        if self.pk is None:
            raise ValidationError(
                "O item precisa estar cadastrado."
            )

        self._validar_venda_aberta()

        self.delete()

        self._atualizar_total_venda()