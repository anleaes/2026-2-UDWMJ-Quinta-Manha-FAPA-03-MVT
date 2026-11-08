from django.shortcuts import render, redirect

from .forms import GrupoMaterialForm


def adicionar_grupo(request):
    template_name = 'grupos_materiais/adicionar_grupo.html'
    context = {}

    if request.method == 'POST':
        form = GrupoMaterialForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('grupos_materiais:listar_grupos')
    else:
        form = GrupoMaterialForm()

    context['form'] = form
    return render(request, template_name, context)