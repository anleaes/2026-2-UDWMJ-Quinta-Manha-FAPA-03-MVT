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
    quantidade = models.PositiveIntegerField('Quantidade')
    custo_unitario = models.DecimalField(
        'Custo Unitário',
        max_digits=10,
        decimal_places=2,
    )
    data_entrada = models.DateTimeField('Data da Entrada', auto_now_add=True)
