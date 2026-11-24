from django.shortcuts import render, redirect

from .forms import VendaForm


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