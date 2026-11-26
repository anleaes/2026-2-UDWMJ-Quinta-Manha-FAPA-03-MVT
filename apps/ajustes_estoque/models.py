from django.core.exceptions import ValidationError
from django.db import models, transaction
from estoques.models import Estoque


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

    def calcular_diferenca(self):
        if (
            type(self.quantidade_anterior) is not int
            or type(self.quantidade_contada) is not int
        ):
            raise ValidationError('Informe as quantidades para calcular a diferença.')

        return self.quantidade_contada - self.quantidade_anterior

    def registrar_ajuste(self):
        if not self._state.adding:
            raise ValidationError('Este ajuste já foi registrado.')

        with transaction.atomic():
            try:
                estoque = Estoque.objects.select_for_update().get(
                    material_id=self.material_id
                )
            except Estoque.DoesNotExist:
                raise ValidationError(
                    'Não existe estoque cadastrado para este material.'
                )

            self.quantidade_anterior = estoque.quantidade
            self.diferenca = self.calcular_diferenca()
            self.full_clean()
            self.save()
            estoque.ajustar_quantidade(self.quantidade_contada)

    class Meta:
        verbose_name = 'Ajuste de Estoque'
        verbose_name_plural = 'Ajustes de Estoque'
        ordering = ['-data_ajuste']

    def __str__(self):
        return f'{self.material} - diferença: {self.diferenca}'
