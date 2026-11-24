from django.db import models

class Venda(models.Model):
    data_venda = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )