from django import forms
from .models import GrupoMaterial


class GrupoMaterialForm(forms.ModelForm):

    class Meta:
        model = GrupoMaterial
        exclude = ()

    def clean(self):
        cleaned_data = super().clean()

        nome = cleaned_data.get('nome')
        segmento = cleaned_data.get('segmento')

        if nome and segmento:
            if GrupoMaterial.objects.filter(
                nome__iexact=nome,
                segmento__iexact=segmento
            ).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(
                    'Este grupo já está cadastrado.'
                )

        return cleaned_data