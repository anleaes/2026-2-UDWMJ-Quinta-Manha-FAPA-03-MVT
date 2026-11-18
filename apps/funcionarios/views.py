from django.shortcuts import render, redirect, get_object_or_404
from .models import Funcionario
from .forms import FuncionarioForm


def adicionar_funcionario(request):
    template_name = 'funcionarios/adicionar_funcionario.html'
    context = {}

    if request.method == 'POST':
        form = FuncionarioForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('funcionarios:listar_funcionarios')
    else:
        form = FuncionarioForm()

    context['form'] = form
    return render(request, template_name, context)


def listar_funcionarios(request):
    template_name = 'funcionarios/listar_funcionarios.html'

    funcionarios = Funcionario.objects.all()

    context = {
        'funcionarios': funcionarios
    }

    return render(request, template_name, context)


def editar_funcionario(request, id_funcionario):
    template_name = 'funcionarios/adicionar_funcionario.html'
    context = {}

    funcionario = get_object_or_404(Funcionario, id=id_funcionario)

    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)

        if form.is_valid():
            form.save()
            return redirect('funcionarios:listar_funcionarios')
    else:
        form = FuncionarioForm(instance=funcionario)

    context['form'] = form
    return render(request, template_name, context)