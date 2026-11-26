from django import forms

from funcionarios.models import Funcionario
from .models import Venda


class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = [
            "comprador",
            "funcionario",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["funcionario"].queryset = (
            Funcionario.objects.filter(ativo=True)
        )