from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from estoques.models import Estoque
from .forms import AjusteEstoqueForm
from .models import AjusteEstoque


def adicionar_ajuste(request, id_estoque=None):
    template_name = 'ajustes_estoque/adicionar_ajuste.html'

    estoque = None
    material = None

    if id_estoque is not None:
        estoque = get_object_or_404(
            Estoque,
            id=id_estoque,
            material__ativo=True,
        )
        material = estoque.material

    if request.method == 'POST':
        form = AjusteEstoqueForm(request.POST, material=material)

        if form.is_valid():
            try:
                ajuste = form.save(commit=False)
                ajuste.registrar_ajuste()

                messages.success(request, 'Ajuste de estoque registrado com sucesso.')

                if estoque is not None:
                    return redirect('estoques:listar_estoques')

                return redirect('ajustes_estoque:listar_ajustes')
            except ValidationError as erro:
                form.add_error(None, erro)
    else:
        form = AjusteEstoqueForm(material=material)

    saldos_estoque = dict(
        Estoque.objects.filter(
            material__ativo=True
        ).values_list('material_id', 'quantidade')
    )

    context = {
        'form': form,
        'saldos_estoque': saldos_estoque,
        'estoque': estoque,
    }
    return render(request, template_name, context)


def listar_ajustes(request):
    template_name = 'ajustes_estoque/listar_ajustes.html'
    ajustes = AjusteEstoque.objects.select_related(
        'material',
        'funcionario',
    ).all()

    context = {
        'ajustes': ajustes,
    }
    return render(request, template_name, context)


def consultar_ajuste(request, id_ajuste):
    template_name = 'ajustes_estoque/consultar_ajuste.html'
    ajuste = get_object_or_404(
        AjusteEstoque.objects.select_related('material', 'funcionario'),
        id=id_ajuste,
    )

    context = {
        'ajuste': ajuste,
    }
    return render(request, template_name, context)
