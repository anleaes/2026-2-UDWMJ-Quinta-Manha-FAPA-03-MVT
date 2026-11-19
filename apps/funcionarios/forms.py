from django import forms
from .models import Funcionario


class FuncionarioForm(forms.ModelForm):

    class Meta:
        model = Funcionario
        exclude = ()

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']

        cpf = cpf.replace('.', '').replace('-', '').strip()

        if not cpf.isdigit() or len(cpf) != 11:
            raise forms.ValidationError(
                'O CPF deve conter 11 números.'
            )

        if len(set(cpf)) == 1:
            raise forms.ValidationError(
                'Informe um CPF válido.'
            )

        if Funcionario.objects.filter(cpf=cpf).exclude(
            pk=self.instance.pk
        ).exists():
            raise forms.ValidationError(
                'Este CPF já está cadastrado.'
            )

        return cpf