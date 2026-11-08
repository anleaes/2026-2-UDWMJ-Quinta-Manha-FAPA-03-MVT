from django.db import models

class GrupoMaterial(models.Model):
    nome = models.CharField(max_length=100)
    segmento = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)