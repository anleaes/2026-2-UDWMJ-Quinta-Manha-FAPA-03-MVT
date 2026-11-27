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

    def __init__(self, *args, venda=None, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields.pop("material")
        else:
            materiais = MaterialPapelaria.objects.filter(
                ativo=True,
                estoque__quantidade__gt=0
            )

            if venda is not None:
                materiais_cadastrados = venda.itens.values_list(
                    "material_id",
                    flat=True
                )

                materiais = materiais.exclude(
                    pk__in=materiais_cadastrados
                )

            self.fields["material"].queryset = materiais