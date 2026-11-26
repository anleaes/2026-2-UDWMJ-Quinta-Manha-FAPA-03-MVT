from django.db import models


class AjusteEstoque(models.Model):
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
    quantidade_anterior = models.PositiveIntegerField('Quantidade Anterior')
    quantidade_contada = models.PositiveIntegerField('Quantidade Contada')
    diferenca = models.IntegerField('Diferença')
    motivo = models.TextField('Motivo')
    data_ajuste = models.DateTimeField('Data do Ajuste', auto_now_add=True)
