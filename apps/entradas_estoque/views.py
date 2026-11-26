from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from .forms import EntradaEstoqueForm


def adicionar_entrada(request):
    template_name = 'entradas_estoque/adicionar_entrada.html'

    if request.method == 'POST':
        form = EntradaEstoqueForm(request.POST)

        if form.is_valid():
            entrada = form.save(commit=False)

            try:
                entrada.registrar_entrada()
                return redirect('entradas_estoque:listar_entradas')
            except ValidationError as erro:
                form.add_error(None, erro)
    else:
        form = EntradaEstoqueForm()

    context = {
        'form': form,
    }

    return render(request, template_name, context)
