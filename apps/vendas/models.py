from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Venda(models.Model):
    class Status(models.TextChoices):
        ABERTA = 'ABERTA', 'Aberta'
        FINALIZADA = 'FINALIZADA', 'Finalizada'
        CANCELADA = 'CANCELADA', 'Cancelada'

    comprador = models.ForeignKey(
        'compradores.Comprador',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    funcionario = models.ForeignKey(
        'funcionarios.Funcionario',
        on_delete=models.PROTECT
    )

    data_venda = models.DateTimeField(auto_now_add=True)

    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )

    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.ABERTA
    )

    def calcular_total(self):
        total = Decimal("0.00")

        for item in self.itens.all():
            total += item.calcular_subtotal()

        return total

    # implementar finalizar_venda() apos a integracao
    # com ItemVenda, Estoque e Pagamento.
    def _validar_finalizacao(self):
        if self.status != self.Status.ABERTA:
            raise ValidationError(
                "Somente vendas abertas podem ser finalizadas."
            )

        if not self.itens.exists():
            raise ValidationError(
                "A venda precisa possuir pelo menos um item."
            )

    # verificar a existencia de pagamento confirmado
    # antes de permitir o cancelamento.
    def cancelar_venda(self):
        if self.status != self.Status.ABERTA:
            raise ValidationError(
                "Somente vendas abertas podem ser canceladas."
            )

        self.status = self.Status.CANCELADA
        self.save(update_fields=["status"])

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
        ordering = ["-data_venda"]

    def __str__(self):
        return f"Venda #{self.id}"