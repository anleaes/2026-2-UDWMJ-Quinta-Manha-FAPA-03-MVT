from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import MaterialPapelariaForm
from .models import MaterialPapelaria


def adicionar_material(request):
    if request.method == 'POST':
        form = MaterialPapelariaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('materiais_papelaria:listar_materiais')
    else:
        form = MaterialPapelariaForm()

    return render(request, 'materiais_papelaria/adicionar_material.html', {'form': form})


def listar_materiais(request):
    materiais = MaterialPapelaria.objects.select_related('grupo', 'marca')
    return render(
        request,
        'materiais_papelaria/listar_materiais.html',
        {'materiais': materiais},
    )


def editar_material(request, id_material):
    material = get_object_or_404(MaterialPapelaria, id=id_material)
    if request.method == 'POST':
        form = MaterialPapelariaForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            return redirect('materiais_papelaria:listar_materiais')
    else:
        form = MaterialPapelariaForm(instance=material)

    return render(request, 'materiais_papelaria/adicionar_material.html', {'form': form})


@require_POST
def excluir_material(request, id_material):
    material = get_object_or_404(MaterialPapelaria, id=id_material)
    material.delete()
    return redirect('materiais_papelaria:listar_materiais')
