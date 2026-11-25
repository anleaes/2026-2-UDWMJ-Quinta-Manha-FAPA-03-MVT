from django import forms
from .models import Fornecedor


class FornecedorForm(forms.ModelForm):

    class Meta:
        model = Fornecedor
        exclude = ()

    def _normalizar_cnpj(self, cnpj):
        return cnpj.replace('.', '').replace('/', '').replace('-', '').strip()

    def clean_cnpj(self):
        cnpj = self._normalizar_cnpj(self.cleaned_data['cnpj'])

        if not cnpj.isdigit() or len(cnpj) != 14:
            raise forms.ValidationError(
                'O CNPJ deve conter 14 números.'
            )

        if len(set(cnpj)) == 1:
            raise forms.ValidationError(
                'Informe um CNPJ válido.'
            )

        fornecedores = Fornecedor.objects.exclude(pk=self.instance.pk)

        for fornecedor in fornecedores:
            cnpj_existente = self._normalizar_cnpj(fornecedor.cnpj)

            if cnpj_existente == cnpj:
                raise forms.ValidationError(
                    'Este CNPJ já está cadastrado.'
                )

        return cnpj

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']

        telefone = telefone.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')

        if not telefone.isdigit() or len(telefone) not in (10, 11):
            raise forms.ValidationError(
                'Número de telefone inválido.'
            )

        return telefone