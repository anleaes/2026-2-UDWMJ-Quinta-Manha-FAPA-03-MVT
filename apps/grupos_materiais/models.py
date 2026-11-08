from django.db import models

class GrupoMaterial(models.Model):
    nome = models.CharField(max_length=100)
    segmento = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    def ativar_grupo(self):
        self.ativo = True
        self.save()

    def desativar_grupo(self):
        self.ativo = False
        self.save()