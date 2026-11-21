
from datetime import date

from django.test import TestCase
from django.urls import reverse, resolve
from django.core.exceptions import ValidationError

from .models import Comprador
from .forms import CompradorForm


class CompradorUrlsTest(TestCase):

    def test_url_listar_compradores(self):
        self.assertEqual(
            reverse('compradores:listar_compradores'),
            '/compradores/listar/'
        )

    def test_url_adicionar_comprador(self):
        self.assertEqual(
            reverse('compradores:adicionar_comprador'),
            '/compradores/adicionar/'
        )

    def test_url_editar_comprador(self):
        self.assertEqual(
            reverse('compradores:editar_comprador', args=[1]),
            '/compradores/editar/1/'
        )

    def test_url_excluir_comprador(self):
        self.assertEqual(
            reverse('compradores:excluir_comprador', args=[1]),
            '/compradores/excluir/1/'
        )

    def test_url_listar_direciona_para_view_correta(self):
        self.assertEqual(
            resolve('/compradores/listar/').func.__name__,
            'listar_compradores'
        )

    def test_url_adicionar_direciona_para_view_correta(self):
        self.assertEqual(
            resolve('/compradores/adicionar/').func.__name__,
            'adicionar_comprador'
        )

    def test_url_editar_direciona_para_view_correta(self):
        self.assertEqual(
            resolve('/compradores/editar/1/').func.__name__,
            'editar_comprador'
        )

    def test_url_excluir_direciona_para_view_correta(self):
        self.assertEqual(
            resolve('/compradores/excluir/1/').func.__name__,
            'excluir_comprador'
        )


class CompradorModelTest(TestCase):

    def setUp(self):
        self.comprador = Comprador.objects.create(
            nome_completo='João da Silva',
            cpf='52998224725',
            telefone_contato='51999999999',
            data_nascimento=date(2000, 5, 15)
        )

    def test_criar_comprador(self):
        self.assertEqual(
            self.comprador.nome_completo,
            'João da Silva'
        )

    def test_validar_cpf_valido(self):
        self.assertTrue(self.comprador.validar_cpf())

    def test_validar_cpf_invalido(self):
        self.comprador.cpf = '11111111111'
        self.assertFalse(self.comprador.validar_cpf())

    def test_validar_cpf_vazio(self):
        self.comprador.cpf = ''
        self.assertFalse(self.comprador.validar_cpf())

    def test_modelo_rejeita_cpf_invalido(self):
        self.comprador.cpf = '11111111111'

        with self.assertRaises(ValidationError):
            self.comprador.full_clean()

    def test_atualizar_cadastro(self):
        self.comprador.atualizar_cadastro(
            nome_completo='Maria da Silva',
            cpf='52998224725',
            telefone_contato='51988888888',
            data_nascimento=date(1998, 3, 10)
        )

        self.comprador.refresh_from_db()

        self.assertEqual(
            self.comprador.nome_completo,
            'Maria da Silva'
        )

    def test_str(self):
        self.assertEqual(
            str(self.comprador),
            'João da Silva'
        )


class CompradorFormTest(TestCase):

    def test_formulario_cpf_invalido(self):
        dados = {
            'nome_completo': 'Maria da Silva',
            'cpf': '11111111111',
            'telefone_contato': '51999999999',
            'data_nascimento': '2000-05-15'
        }

        form = CompradorForm(data=dados)

        self.assertFalse(form.is_valid())
        self.assertIn('cpf', form.errors)


class CompradorViewsTest(TestCase):

    def setUp(self):
        self.comprador = Comprador.objects.create(
            nome_completo='João da Silva',
            cpf='52998224725',
            telefone_contato='51999999999',
            data_nascimento=date(2000, 5, 15)
        )

    def test_listar_compradores(self):
        response = self.client.get(
            reverse('compradores:listar_compradores')
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'João da Silva')

    def test_adicionar_comprador(self):
        dados = {
            'nome_completo': 'Maria da Silva',
            'cpf': '11144477735',
            'telefone_contato': '51988888888',
            'data_nascimento': '1998-03-10'
        }

        response = self.client.post(
            reverse('compradores:adicionar_comprador'),
            dados
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Comprador.objects.filter(cpf='11144477735').exists()
        )

    def test_editar_comprador(self):
        dados = {
            'nome_completo': 'João Atualizado',
            'cpf': '52998224725',
            'telefone_contato': '51988888888',
            'data_nascimento': '2000-05-15'
        }

        response = self.client.post(
            reverse(
                'compradores:editar_comprador',
                args=[self.comprador.id]
            ),
            dados
        )

        self.assertEqual(response.status_code, 302)

        self.comprador.refresh_from_db()

        self.assertEqual(
            self.comprador.nome_completo,
            'João Atualizado'
        )

    def test_excluir_comprador(self):
        response = self.client.post(
            reverse(
                'compradores:excluir_comprador',
                args=[self.comprador.id]
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Comprador.objects.filter(id=self.comprador.id).exists()
        )

    def test_editar_comprador_inexistente(self):
        response = self.client.get(
            reverse(
                'compradores:editar_comprador',
                args=[9999]
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_excluir_comprador_inexistente(self):
        response = self.client.get(
            reverse(
                'compradores:excluir_comprador',
                args=[9999]
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_excluir_comprador_por_get_nao_exclui(self):
        response = self.client.get(
            reverse(
                'compradores:excluir_comprador',
                args=[self.comprador.id]
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Comprador.objects.filter(id=self.comprador.id).exists()
        )
