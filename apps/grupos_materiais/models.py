from django.db import models

class GrupoMaterial(models.Model):
    nome = models.CharField(max_length=100)
    segmento = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    def atualizar_grupo(self, nome, segmento):
        self.nome = nome
        self.segmento = segmento
        self.save()

    def ativar_grupo(self):
        self.ativo = True
        self.save()

    def desativar_grupo(self):
        self.ativo = False
        self.save()

    class Meta:
        verbose_name = "Grupo de Material"
        verbose_name_plural = "Grupos de Materiais"
        ordering = ["nome"]

    def __str__(self):
        return self.nome