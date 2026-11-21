
from django.db import models
from django.core.exceptions import ValidationError


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

    data_cadastro = models.DateField(
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
        cpf = ''.join(filter(str.isdigit, self.cpf or ''))

        if len(cpf) != 11:
            return False

        if cpf == cpf[0] * 11:
            return False

        soma = sum(
            int(cpf[i]) * (10 - i)
            for i in range(9)
        )

        resto = (soma * 10) % 11
        digito1 = 0 if resto == 10 else resto

        if digito1 != int(cpf[9]):
            return False

        soma = sum(
            int(cpf[i]) * (11 - i)
            for i in range(10)
        )

        resto = (soma * 10) % 11
        digito2 = 0 if resto == 10 else resto

        return digito2 == int(cpf[10])

    def clean(self):
        super().clean()

        if not self.validar_cpf():
            raise ValidationError({
                'cpf': 'Informe um CPF válido.'
            })

    class Meta:
        verbose_name = 'Comprador'
        verbose_name_plural = 'Compradores'
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo
