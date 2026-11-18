from django.db import models

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    cargo = models.CharField(max_length=100)
    data_admissao = models.DateField()
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ["nome"]

    def __str__(self):
        return self.nome