from django import forms

from fornecedores.models import Fornecedor
from funcionarios.models import Funcionario
from materiais_papelaria.models import MaterialPapelaria
from .models import EntradaEstoque


class EntradaEstoqueForm(forms.ModelForm):

    class Meta:
        model = EntradaEstoque
        fields = [
            'fornecedor',
            'material',
            'funcionario',
            'quantidade',
            'custo_unitario',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fornecedor'].queryset = Fornecedor.objects.filter(ativo=True)
        self.fields['material'].queryset = MaterialPapelaria.objects.filter(ativo=True)
        self.fields['funcionario'].queryset = Funcionario.objects.filter(ativo=True)
