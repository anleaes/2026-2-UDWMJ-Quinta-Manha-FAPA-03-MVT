from django import forms
from .models import Estoque


class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['material', 'estoque_minimo', 'localizacao']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # na edição de um estoque, o campo material deve ser desabilitado para evitar alterações
        if self.instance and self.instance.pk:
            self.fields['material'].disabled = True


class MovimentarEstoqueForm(forms.Form):
    OPERACOES = [
        ('adicionar', 'Adicionar quantidade'),
        ('retirar', 'Retirar quantidade'),
        ('ajustar', 'Ajustar quantidade'),
    ]

    operacao = forms.ChoiceField(
        choices=OPERACOES,
        label='Tipo de operação'
    )

    quantidade = forms.IntegerField(
        min_value=0,
        label='Quantidade'
    )