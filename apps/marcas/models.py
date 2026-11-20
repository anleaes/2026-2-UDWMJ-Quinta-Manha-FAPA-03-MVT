from django.db import models

# Create your models here.

class Marca(models.Model):
    nome = models.CharField('Nome', max_length=50)
    descricao = models.TextField('Descricao', max_length=200)
    pais_origem = models.CharField('País de Origem', max_length=50)
    ativo = models.BooleanField('Ativo', default=True)

    def atualizar_dados(self, nome, descricao, pais_origem):
        self.nome = nome
        self.descricao = descricao
        self.pais_origem = pais_origem
        self.save()

    def ativar(self):
        self.ativo = True
        self.save()

    def desativar(self):
        self.ativo = False
        self.save()

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ["nome"]

    def __str__(self):
        return self.nome