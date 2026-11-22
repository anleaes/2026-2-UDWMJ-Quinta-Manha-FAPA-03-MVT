from django.shortcuts import redirect, render

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
