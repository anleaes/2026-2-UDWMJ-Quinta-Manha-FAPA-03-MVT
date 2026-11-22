from django import forms

from .models import MaterialPapelaria


class MaterialPapelariaForm(forms.ModelForm):
    class Meta:
        model = MaterialPapelaria
        fields = '__all__'
