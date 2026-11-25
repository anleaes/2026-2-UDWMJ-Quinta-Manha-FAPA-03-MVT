from django import forms

from grupos_materiais.models import GrupoMaterial
from marcas.models import Marca
from .models import MaterialPapelaria


class MaterialPapelariaForm(forms.ModelForm):
    class Meta:
        model = MaterialPapelaria
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['grupo'].queryset = (
            GrupoMaterial.objects.filter(ativo=True) |
            GrupoMaterial.objects.filter(pk=self.instance.grupo_id)
        )

        self.fields['marca'].queryset = (
            Marca.objects.filter(ativo=True) |
            Marca.objects.filter(pk=self.instance.marca_id)
        )