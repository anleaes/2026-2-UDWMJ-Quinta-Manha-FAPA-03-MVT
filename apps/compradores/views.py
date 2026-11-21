from django.shortcuts import render, redirect, get_object_or_404

from .models import Comprador
from .forms import CompradorForm
from django.contrib import messages

def adicionar_comprador(request):
    template_name = 'compradores/adicionar_comprador.html'

    if request.method == 'POST':
        form = CompradorForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Comprador cadastrado com sucesso!')
            return redirect('compradores:listar_compradores')
    else:
        form = CompradorForm()

    context = {
        'form': form
    }

    return render(request, template_name, context)


def listar_compradores(request):
    template_name = 'compradores/listar_compradores.html'

    compradores = Comprador.objects.all()

    context = {
        'compradores': compradores
    }

    return render(request, template_name, context)


def editar_comprador(request, id_comprador):
    template_name = 'compradores/adicionar_comprador.html'

    comprador = get_object_or_404(Comprador, id=id_comprador)

    if request.method == 'POST':
        form = CompradorForm(request.POST, instance=comprador)

        if form.is_valid():
            form.save()
            return redirect('compradores:listar_compradores')
    else:
        form = CompradorForm(instance=comprador)

    context = {
        'form': form
    }

    return render(request, template_name, context)


def excluir_comprador(request, id_comprador):
    comprador = get_object_or_404(Comprador, id=id_comprador)

    if request.method == 'POST':
        comprador.delete()
        return redirect('compradores:listar_compradores')

    context = {
        'comprador': comprador
    }

    return render(
        request,
        'compradores/excluir_comprador.html',
        context
    )
