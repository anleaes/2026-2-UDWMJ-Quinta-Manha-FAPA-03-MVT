from django.db import models


class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    ativo = models.BooleanField(default=True)

    def atualizar_dados(self, nome, cnpj, telefone, email):
        self.nome = nome
        self.cnpj = cnpj
        self.telefone = telefone
        self.email = email
        self.save()

    def ativar(self):
        self.ativo = True
        self.save()

    def desativar(self):
        self.ativo = False
        self.save()
