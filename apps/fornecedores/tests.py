from django.test import TestCase
from django.urls import reverse
from .models import Fornecedor


class FornecedorModelTests(TestCase):

    def setUp(self):
        self.fornecedor = Fornecedor.objects.create(
            nome='Fornecedor de Teste',
            cnpj='12.345.678/0001-90',
            telefone='(51) 3333-2222',
            email='contato@example.com',
        )

    def test_atualizar_dados(self):
        self.fornecedor.atualizar_dados(
            'Novo Fornecedor',
            '98.765.432/0001-10',
            '(51) 9999-8888',
            'novo@example.com',
        )
        self.fornecedor.refresh_from_db()

        self.assertEqual(self.fornecedor.nome, 'Novo Fornecedor')
        self.assertEqual(self.fornecedor.cnpj, '98.765.432/0001-10')
        self.assertEqual(self.fornecedor.telefone, '(51) 9999-8888')
        self.assertEqual(self.fornecedor.email, 'novo@example.com')

    def test_ativar(self):
        self.fornecedor.desativar()
        self.fornecedor.ativar()
        self.fornecedor.refresh_from_db()

        self.assertTrue(self.fornecedor.ativo)

    def test_desativar(self):
        self.fornecedor.desativar()
        self.fornecedor.refresh_from_db()

        self.assertFalse(self.fornecedor.ativo)


class FornecedorViewsTests(TestCase):

    def setUp(self):
        self.fornecedor = Fornecedor.objects.create(
            nome='Fornecedor de Teste',
            cnpj='12.345.678/0001-90',
            telefone='(51) 3333-2222',
            email='contato@example.com',
        )

    def test_cadastrar_fornecedor(self):
        response = self.client.post(reverse('fornecedores:adicionar_fornecedor'), {
            'nome': 'Novo Fornecedor',
            'cnpj': '98.765.432/0001-10',
            'telefone': '(51) 9999-8888',
            'email': 'novo@example.com',
            'ativo': True,
        })

        self.assertRedirects(response, reverse('fornecedores:listar_fornecedores'))
        self.assertTrue(Fornecedor.objects.filter(nome='Novo Fornecedor').exists())

    def test_listar_fornecedores(self):
        response = self.client.get(reverse('fornecedores:listar_fornecedores'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.fornecedor.nome)

    def test_editar_fornecedor(self):
        response = self.client.post(
            reverse('fornecedores:editar_fornecedor', args=[self.fornecedor.id]),
            {
                'nome': 'Fornecedor Editado',
                'cnpj': self.fornecedor.cnpj,
                'telefone': self.fornecedor.telefone,
                'email': self.fornecedor.email,
                'ativo': True,
            },
        )

        self.assertRedirects(response, reverse('fornecedores:listar_fornecedores'))
        self.fornecedor.refresh_from_db()
        self.assertEqual(self.fornecedor.nome, 'Fornecedor Editado')

    def test_excluir_fornecedor(self):
        response = self.client.post(
            reverse('fornecedores:excluir_fornecedor', args=[self.fornecedor.id])
        )

        self.assertRedirects(response, reverse('fornecedores:listar_fornecedores'))
        self.assertFalse(Fornecedor.objects.filter(id=self.fornecedor.id).exists())
