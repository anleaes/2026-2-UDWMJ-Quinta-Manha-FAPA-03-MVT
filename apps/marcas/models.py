from django.db import models

# Create your models here.

class Marca(models.Model):
    nome = models.CharField('Nome', max_length=50)
    descricao = models.TextField('Descricao', max_length=200)
    pais_origem = models.CharField('País de Origem', max_length=50)
    ativo = models.BooleanField('Ativo', default=False)
