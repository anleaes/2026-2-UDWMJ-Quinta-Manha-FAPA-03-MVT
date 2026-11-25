from django.db import models
from django.core.exceptions import ValidationError
from materiais_papelaria.models import MaterialPapelaria

# Create your models here.

class Estoque(models.Model):
    material = models.OneToOneField( # um estoque para um material
        MaterialPapelaria,
        on_delete=models.PROTECT, # impede a exclusão do material se houver estoque associado
        related_name='estoque'
    )

    quantidade = models.PositiveIntegerField(default=0) 
    estoque_minimo = models.PositiveIntegerField(default=0)
    localizacao = models.CharField(max_length=100)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    class Meta: # define os nomes amigáveis e ordena por id
        verbose_name = 'Estoque'
        verbose_name_plural = 'Estoques'
        ordering = ['id']

    def __str__(self): 
        return f'{self.material} - Saldo: {self.quantidade}'

    def adicionar_quantidade(self, qtd):
        if type(qtd) is not int or qtd <= 0:
            raise ValidationError('Informe uma quantidade inteira maior que zero.')

        self.quantidade += qtd
        self.save(update_fields=['quantidade', 'ultima_atualizacao'])

    def retirar_quantidade(self, qtd):
        if type(qtd) is not int or qtd <= 0:
            raise ValidationError('Informe uma quantidade inteira maior que zero.')

        if qtd > self.quantidade:
            raise ValidationError('Saldo insuficiente em estoque.')

        self.quantidade -= qtd
        self.save(update_fields=['quantidade', 'ultima_atualizacao'])

    def ajustar_quantidade(self, nova_qtd):
        if type(nova_qtd) is not int or nova_qtd < 0:
            raise ValidationError('Informe uma quantidade inteira não negativa.')

        self.quantidade = nova_qtd
        self.save(update_fields=['quantidade', 'ultima_atualizacao'])