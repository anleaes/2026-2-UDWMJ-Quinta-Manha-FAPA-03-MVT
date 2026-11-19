from django.db import models

# Create your models here.

class Marca(models.Model):
    nome = models.CharField('Nome', max_length=50)
    descricao = models.TextField('Descricao', max_length=200)
    pais_origem = models.CharField('País de Origem', max_length=50)
    ativo = models.BooleanField('Ativo', default=False)

    def atualizar_marca(self, nome, segmento):
        self.nome = nome
        self.segmento = segmento
        self.save()

    def ativar_marca(self):
        self.ativo = True
        self.save()

    def desativar_marca(self):
        self.ativo = False
        self.save()

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ["nome"]