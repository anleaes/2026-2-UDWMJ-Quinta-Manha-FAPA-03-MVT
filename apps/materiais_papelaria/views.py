from django.shortcuts import redirect, render

from .forms import MaterialPapelariaForm


def adicionar_material(request):
    if request.method == 'POST':
        form = MaterialPapelariaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('materiais_papelaria:listar_materiais')
    else:
        form = MaterialPapelariaForm()

    return render(request, 'materiais_papelaria/adicionar_material.html', {'form': form})
