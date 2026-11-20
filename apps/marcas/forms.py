from django import forms
from .models import Marca


class MarcaForm(forms.ModelForm):

    class Meta:
        model = Marca
        exclude = ()
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }