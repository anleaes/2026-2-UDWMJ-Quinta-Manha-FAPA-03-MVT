from django import forms

from materiais_papelaria.models import MaterialPapelaria
from .models import ItemVenda


class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = [
            "material",
            "quantidade",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["material"].queryset = (
            MaterialPapelaria.objects.filter(ativo=True)
        )