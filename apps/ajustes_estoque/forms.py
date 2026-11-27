from django import forms

from funcionarios.models import Funcionario
from materiais_papelaria.models import MaterialPapelaria
from .models import AjusteEstoque


class AjusteEstoqueForm(forms.ModelForm):
    quantidade_contada = forms.IntegerField(
        min_value=0,
        label='Quantidade Contada',
    )
    motivo = forms.CharField(
        strip=True,
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Motivo',
    )

    class Meta:
        model = AjusteEstoque
        fields = [
            'material',
            'funcionario',
            'quantidade_contada',
            'motivo',
        ]

    def __init__(self, *args, material=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].queryset = MaterialPapelaria.objects.filter(
            ativo=True,
            estoque__isnull=False,
        )
        self.fields['funcionario'].queryset = Funcionario.objects.filter(ativo=True)

        if material is not None:
            self.initial['material'] = material.pk
            self.fields['material'].disabled = True

    def clean_motivo(self):
        motivo = self.cleaned_data['motivo']
        if not motivo.strip():
            raise forms.ValidationError('Informe o motivo do ajuste.')
        return motivo
