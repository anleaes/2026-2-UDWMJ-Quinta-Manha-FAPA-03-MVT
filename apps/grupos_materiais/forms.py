from django import forms
from .models import GrupoMaterial


class GrupoMaterialForm(forms.ModelForm):

    class Meta:
        model = GrupoMaterial
        exclude = ()