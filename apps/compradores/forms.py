from django import forms
from django.utils import timezone
from .models import Comprador


class CompradorForm(forms.ModelForm):

    class Meta:
        model = Comprador
        exclude = ()

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf'].strip()

        comprador = Comprador(cpf=cpf)

        if not comprador.validar_cpf():
            raise forms.ValidationError(
                'O CPF deve conter 11 números válidos.'
            )

        return cpf

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data['data_nascimento']

        if data_nascimento > timezone.localdate():
            raise forms.ValidationError(
                'Data de nascimento inválida.'
            )

        return data_nascimento