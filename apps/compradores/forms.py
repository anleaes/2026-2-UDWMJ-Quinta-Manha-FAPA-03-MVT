from django import forms
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