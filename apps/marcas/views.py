from django.shortcuts import render, redirect, get_object_or_404
from .models import Marca
from .forms import MarcaForm
from django.views.decorators.http import require_POST


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

def listar_marcas(request):
    template_name = 'marcas/listar_marcas.html'

    marcas = Marca.objects.all()

    context = {
        'marcas': marcas
    }

    return render(request, template_name, context)

def editar_marca(request, id_marca):
    template_name = 'marcas/adicionar_marca.html'
    context = {}

    marca = get_object_or_404(Marca, id=id_marca)

    if request.method == 'POST':
        form = MarcaForm(request.POST, instance=marca)

        if form.is_valid():
            form.save()
            return redirect('marcas:listar_marcas')
    else:
        form = MarcaForm(instance=marca)

    context['form'] = form
    return render(request, template_name, context)

@require_POST
def excluir_marca(request, id_marca):
    marca = get_object_or_404(Marca, id=id_marca)

    marca.delete()

    return redirect('marcas:listar_marcas')