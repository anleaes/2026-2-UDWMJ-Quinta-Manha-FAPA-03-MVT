from django.db import models

class Venda(models.Model):
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
        default=0
    )