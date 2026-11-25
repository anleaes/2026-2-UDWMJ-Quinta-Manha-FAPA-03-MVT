from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from .forms import EstoqueForm
from .models import Estoque

# Create your views here.

def adicionar_estoque(request):
    template_name = 'estoques/adicionar_estoque.html'
    if request.method == 'POST':
        form = EstoqueForm(request.POST)
        if form.is_valid():
            material = form.cleaned_data['material']
            if Estoque.objects.filter(material=material).exists():
                form.add_error('material', 'Já existe um registro de estoque para este material.')
            else:
                try:
                    estoque = form.save(commit=False)
                    estoque.quantidade = 0
                    estoque.save()
                    return redirect('estoques:listar_estoques')
                except ValidationError as exc:
                    form.add_error(None, exc.message)
    else:
        form = EstoqueForm()

    context = {
        'form': form,
        'editando': False,
    }
    return render(request, template_name, context)

