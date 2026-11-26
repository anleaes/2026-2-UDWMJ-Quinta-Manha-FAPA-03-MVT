from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError

from .forms import VendaForm
from .models import Venda


def adicionar_venda(request):
    template_name = 'vendas/adicionar_venda.html'
    context = {}

    if request.method == 'POST':
        form = VendaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('vendas:listar_vendas')
    else:
        form = VendaForm()

    context['form'] = form
    return render(request, template_name, context)


def listar_vendas(request):
    template_name = 'vendas/listar_vendas.html'
    vendas = Venda.objects.all()

    context = {
        'vendas': vendas
    }

    return render(request, template_name, context)


def detalhar_venda(request, id_venda):
    template_name = 'vendas/detalhar_venda.html'

    venda = get_object_or_404(Venda, id=id_venda)

    context = {
        'venda': venda
    }

    return render(request, template_name, context)
    

def editar_venda(request, id_venda):
    template_name = 'vendas/adicionar_venda.html'
    context = {}

    venda = get_object_or_404(Venda, id=id_venda)

    if venda.status != Venda.Status.ABERTA:
        return redirect('vendas:detalhar_venda', id_venda=id_venda)

    if request.method == 'POST':
        form = VendaForm(request.POST, instance=venda)

        if form.is_valid():
            try:
                venda.atualizar_dados(
                    comprador=form.cleaned_data['comprador'],
                    funcionario=form.cleaned_data['funcionario']
                )

                return redirect('vendas:detalhar_venda', id_venda=id_venda)

            except ValidationError as erro:
                form.add_error(None, erro)
    else:
        form = VendaForm(instance=venda)

    context['form'] = form
    context['venda'] = venda

    return render(request, template_name, context)


@require_POST
def cancelar_venda(request, id_venda):
    venda = get_object_or_404(Venda, id=id_venda)

    try:
        venda.cancelar_venda()
    except ValidationError as erro:
        template_name = 'vendas/detalhar_venda.html'

        context = {
            'venda': venda,
            'erro': erro.messages[0]
        }

        return render(request, template_name, context)

    return redirect('vendas:detalhar_venda', id_venda=id_venda)