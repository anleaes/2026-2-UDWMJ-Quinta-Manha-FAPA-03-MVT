from django import forms
from .models import Funcionario
from django.utils import timezone


class FuncionarioForm(forms.ModelForm):

    class Meta:
        model = Funcionario
        exclude = ()

        widgets = {
        'data_admissao': forms.DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'}
        )
    }

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
    

    def clean_data_admissao(self):
        data_admissao = self.cleaned_data['data_admissao']

        if data_admissao > timezone.localdate():
            raise forms.ValidationError(
                'A data de admissão não pode ser futura.'
            )

        return data_admissao
