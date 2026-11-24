from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError

from vendas.models import Venda
from .forms import ItemVendaForm


def adicionar_item(request, id_venda):
    template_name = 'itens_venda/adicionar_item.html'

    venda = get_object_or_404(Venda, id=id_venda)

    if venda.status != Venda.Status.ABERTA:
        return redirect('vendas:detalhar_venda', id_venda)

    form = ItemVendaForm(request.POST if request.method == 'POST' else None)

    if request.method == 'POST' and form.is_valid():
        item = form.save(commit=False)
        item.venda = venda

        try:
            item.adicionar_item()
            return redirect('itens_venda:listar_itens', id_venda)
        except ValidationError as erro:
            form.add_error(None, erro.messages)

    context = {
        'form': form,
        'venda': venda,
    }

    return render(request, template_name, context)