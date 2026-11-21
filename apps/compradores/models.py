from django.db import models

class Comprador(models.Model):
    nome_completo = models.CharField(
        max_length=150,
        verbose_name='Nome completo'
    )

    cpf = models.CharField(
        max_length=11,
        unique=True,
        verbose_name='CPF'
    )

    telefone_contato = models.CharField(
        max_length=20,
        verbose_name='Telefone de contato'
    )

    data_nascimento = models.DateField(
        verbose_name='Data de nascimento'
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de cadastro'
    )

    def atualizar_cadastro(
        self,
        nome_completo,
        cpf,
        telefone_contato,
        data_nascimento
    ):
        self.nome_completo = nome_completo
        self.cpf = cpf
        self.telefone_contato = telefone_contato
        self.data_nascimento = data_nascimento
        self.save()

    def validar_cpf(self):
        cpf = self.cpf or ''

        if not cpf.isdigit() or len(cpf) != 11:
            return False

        if len(set(cpf)) == 1:
            return False

        return True

    class Meta:
        verbose_name = 'Comprador'
        verbose_name_plural = 'Compradores'
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo
