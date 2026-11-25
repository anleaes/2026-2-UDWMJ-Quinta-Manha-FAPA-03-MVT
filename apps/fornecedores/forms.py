from django import forms
from .models import Fornecedor


class FornecedorForm(forms.ModelForm):

    class Meta:
        model = Fornecedor
        exclude = ()

    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']

        cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '').strip()

        if not cnpj.isdigit() or len(cnpj) != 14:
            raise forms.ValidationError(
                'O CNPJ deve conter 14 números.'
            )

        if len(set(cnpj)) == 1:
            raise forms.ValidationError(
                'Informe um CNPJ válido.'
            )

        return cnpj