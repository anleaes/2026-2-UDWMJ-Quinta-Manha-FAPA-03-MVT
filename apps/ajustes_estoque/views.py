from uuid import uuid4

from django.contrib import messages
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from estoques.models import Estoque
from .forms import AjusteEstoqueForm
from .models import AjusteEstoque

TOKEN_SESSION_KEY = 'ajustes_estoque_tokens'


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
    if token not in dados.get(TOKEN_SESSION_KEY, []):
        return None

    return session, dados


def _usar_token(request, session, dados, token):
    tokens = dados.get(TOKEN_SESSION_KEY, [])
    tokens.remove(token)
    dados[TOKEN_SESSION_KEY] = tokens
    session.session_data = SessionStore().encode(dados)
    session.save(update_fields=['session_data'])
    request.session[TOKEN_SESSION_KEY] = tokens


def adicionar_ajuste(request):
    template_name = 'ajustes_estoque/adicionar_ajuste.html'

    if request.method == 'POST':
        form = AjusteEstoqueForm(request.POST)
        idempotency_token = request.POST.get('idempotency_token', '')
        if form.is_valid():
            try:
                with transaction.atomic():
                    dados_sessao = _token_pendente(request, idempotency_token)
                    if dados_sessao is None:
                        messages.warning(
                            request,
                            'Este formulário já foi enviado. Confira a listagem de ajustes.',
                        )
                        return redirect('ajustes_estoque:listar_ajustes')

                    session, dados = dados_sessao
                    ajuste = form.save(commit=False)
                    ajuste.registrar_ajuste()
                    _usar_token(request, session, dados, idempotency_token)

                messages.success(request, 'Ajuste de estoque registrado com sucesso.')
                return redirect('ajustes_estoque:listar_ajustes')
            except ValidationError as erro:
                form.add_error(None, erro)
    else:
        form = AjusteEstoqueForm()
        idempotency_token = _novo_token(request)

    if not idempotency_token:
        idempotency_token = _novo_token(request)

    estoques = Estoque.objects.filter(material__ativo=True).select_related('material')
    saldos_estoque = {
        estoque.material_id: estoque.quantidade
        for estoque in estoques
    }

    context = {
        'form': form,
        'saldos_estoque': saldos_estoque,
        'idempotency_token': idempotency_token,
    }
    return render(request, template_name, context)


def listar_ajustes(request):
    template_name = 'ajustes_estoque/listar_ajustes.html'
    ajustes = AjusteEstoque.objects.select_related(
        'material',
        'funcionario',
    ).all()

    context = {
        'ajustes': ajustes,
    }
    return render(request, template_name, context)


def consultar_ajuste(request, id_ajuste):
    template_name = 'ajustes_estoque/consultar_ajuste.html'
    ajuste = get_object_or_404(
        AjusteEstoque.objects.select_related('material', 'funcionario'),
        id=id_ajuste,
    )

    context = {
        'ajuste': ajuste,
    }
    return render(request, template_name, context)
