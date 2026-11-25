from django import forms
from .models import Marca


class MarcaForm(forms.ModelForm):

    class Meta:
        model = Marca
        exclude = ()
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }

    def clean_nome(self):
        nome = self.cleaned_data['nome']

        if Marca.objects.filter(nome__iexact=nome).exclude(
            pk=self.instance.pk
        ).exists():
            raise forms.ValidationError(
                'Esta marca já está cadastrada.'
            )

        return nome