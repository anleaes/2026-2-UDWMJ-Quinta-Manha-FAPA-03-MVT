from django.shortcuts import render, redirect, get_object_or_404
from .models import Fornecedor
from .forms import FornecedorForm


def adicionar_fornecedor(request):
    template_name = 'fornecedores/adicionar_fornecedor.html'
    context = {}

    if request.method == 'POST':
        form = FornecedorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('fornecedores:listar_fornecedores')
    else:
        form = FornecedorForm()

    context['form'] = form
    return render(request, template_name, context)


def listar_fornecedores(request):
    template_name = 'fornecedores/listar_fornecedores.html'
    fornecedores = Fornecedor.objects.all()

    context = {
        'fornecedores': fornecedores
    }

    return render(request, template_name, context)
