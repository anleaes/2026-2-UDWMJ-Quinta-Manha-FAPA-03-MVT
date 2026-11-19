from django.shortcuts import render, redirect, get_object_or_404
from .models import Marca
from .forms import MarcaForm


def adicionar_marca(request):
    template_name = 'marcas/adicionar_marca.html'
    context = {}

    if request.method == 'POST':
        form = MarcaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('marcas:listar_marcas')
    else:
        form = MarcaForm()

    context['form'] = form
    return render(request, template_name, context)

