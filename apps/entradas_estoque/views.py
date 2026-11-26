from uuid import uuid4

from django.contrib import messages
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from .forms import EntradaEstoqueForm
from .models import EntradaEstoque

TOKEN_SESSION_KEY = 'entradas_estoque_tokens'


def _novo_token(request):
    token = uuid4().hex
    tokens = request.session.get(TOKEN_SESSION_KEY, [])
    tokens.append(token)
    request.session[TOKEN_SESSION_KEY] = tokens[-20:]
    return token


def _token_pendente(request, token):
    session_key = request.session.session_key
    if not session_key or not token:
        return None

    session = Session.objects.select_for_update().filter(
        session_key=session_key
    ).first()
    if session is None:
        return None

    dados = session.get_decoded()
    tokens = dados.get(TOKEN_SESSION_KEY, [])
    if token not in tokens:
        return None

    return session, dados


def _usar_token(request, session, dados, token):
    tokens = dados.get(TOKEN_SESSION_KEY, [])
    tokens.remove(token)
    dados[TOKEN_SESSION_KEY] = tokens

    session.session_data = SessionStore().encode(dados)
    session.save(update_fields=['session_data'])
    request.session[TOKEN_SESSION_KEY] = tokens


def adicionar_entrada(request):
    template_name = 'entradas_estoque/adicionar_entrada.html'

    if request.method == 'POST':
        form = EntradaEstoqueForm(request.POST)
        idempotency_token = request.POST.get('idempotency_token', '')

        if form.is_valid():
            try:
                with transaction.atomic():
                    dados_sessao = _token_pendente(request, idempotency_token)
                    if dados_sessao is None:
                        messages.warning(
                            request,
                            'Este formulário já foi enviado. Confira a listagem de entradas.',
                        )
                        return redirect('entradas_estoque:listar_entradas')

                    session, dados = dados_sessao
                    entrada = form.save(commit=False)
                    entrada.registrar_entrada()
                    _usar_token(request, session, dados, idempotency_token)

                messages.success(request, 'Entrada de estoque registrada com sucesso.')
                return redirect('entradas_estoque:listar_entradas')
            except ValidationError as erro:
                form.add_error(None, erro)
    else:
        form = EntradaEstoqueForm()
        idempotency_token = _novo_token(request)

    if not idempotency_token:
        idempotency_token = _novo_token(request)

    context = {
        'form': form,
        'idempotency_token': idempotency_token,
    }

    return render(request, template_name, context)


def listar_entradas(request):
    template_name = 'entradas_estoque/listar_entradas.html'
    entradas = EntradaEstoque.objects.select_related(
        'fornecedor',
        'material',
        'funcionario',
    ).all()

    context = {
        'entradas': entradas,
    }

    return render(request, template_name, context)


def consultar_entrada(request, id_entrada):
    template_name = 'entradas_estoque/consultar_entrada.html'
    entrada = get_object_or_404(
        EntradaEstoque.objects.select_related(
            'fornecedor',
            'material',
            'funcionario',
        ),
        id=id_entrada,
    )

    context = {
        'entrada': entrada,
    }

    return render(request, template_name, context)
