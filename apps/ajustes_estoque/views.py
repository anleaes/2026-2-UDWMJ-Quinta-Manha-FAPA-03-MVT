from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from estoques.models import Estoque
from .forms import AjusteEstoqueForm


def adicionar_ajuste(request):
    template_name = 'ajustes_estoque/adicionar_ajuste.html'

    if request.method == 'POST':
        form = AjusteEstoqueForm(request.POST)
        if form.is_valid():
            try:
                ajuste = form.save(commit=False)
                ajuste.registrar_ajuste()
                return redirect('ajustes_estoque:listar_ajustes')
            except ValidationError as erro:
                form.add_error(None, erro)
    else:
        form = AjusteEstoqueForm()

    estoques = Estoque.objects.filter(material__ativo=True).select_related('material')
    saldos_estoque = {
        estoque.material_id: estoque.quantidade
        for estoque in estoques
    }

    context = {
        'form': form,
        'saldos_estoque': saldos_estoque,
    }
    return render(request, template_name, context)
