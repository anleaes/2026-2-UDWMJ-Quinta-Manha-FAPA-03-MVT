from django.db import models

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    cargo = models.CharField(max_length=100)
    data_admissao = models.DateField()
    ativo = models.BooleanField(default=True)

    def atualizar_dados(self, nome, cpf, cargo, data_admissao):
        self.nome = nome
        self.cpf = cpf
        self.cargo = cargo
        self.data_admissao = data_admissao
        self.save()

    def ativar(self):
        self.ativo = True
        self.save()

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ["nome"]

    def __str__(self):
        return self.nome