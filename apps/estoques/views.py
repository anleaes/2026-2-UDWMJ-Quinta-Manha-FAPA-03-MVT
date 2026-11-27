from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from .forms import EstoqueForm, MovimentarEstoqueForm
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


def listar_estoques(request):
    template_name = 'estoques/listar_estoques.html'
    estoques = Estoque.objects.select_related('material').all()
    context = {
        'estoques': estoques,
    }
    return render(request, template_name, context)


def editar_estoque(request, id_estoque):
    template_name = 'estoques/adicionar_estoque.html'
    estoque = get_object_or_404(Estoque.objects.select_related('material'), id=id_estoque)

    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            try:
                editado = form.save(commit=False)
                editado.save(
                    update_fields=[
                        'estoque_minimo',
                        'localizacao',
                        'ultima_atualizacao'
                    ]
                )
                return redirect('estoques:listar_estoques')
            except ValidationError as exc:
                form.add_error(None, exc.message)
    else:
        form = EstoqueForm(instance=estoque)

    context = {
        'form': form,
        'estoque': estoque,
        'editando': True,
    }
    return render(request, template_name, context)


def consultar_estoque(request, id_estoque):
    template_name = 'estoques/consultar_estoque.html'
    estoque = get_object_or_404(Estoque.objects.select_related('material'), id=id_estoque)
    context = {
        'estoque': estoque,
    }
    return render(request, template_name, context)


def movimentar_estoque(request, id_estoque):
    template_name = 'estoques/movimentar_estoque.html'
    estoque = get_object_or_404(Estoque.objects.select_related('material'), id=id_estoque)

    if request.method == 'POST':
        form = MovimentarEstoqueForm(request.POST)

        if form.is_valid():
            operacao = form.cleaned_data['operacao']
            quantidade = form.cleaned_data['quantidade']

            try:
                if operacao == 'adicionar':
                    estoque.adicionar_quantidade(quantidade)

                elif operacao == 'retirar':
                    estoque.retirar_quantidade(quantidade)

                return redirect('estoques:listar_estoques')

            except ValidationError as exc:
                form.add_error('quantidade', exc)

    else:
        form = MovimentarEstoqueForm()

    context = {
        'form': form,
        'estoque': estoque,
    }
    return render(request, template_name, context)