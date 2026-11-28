
from datetime import date
from decimal import Decimal
from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from PIL import Image

from ajustes_estoque.models import AjusteEstoque
from estoques.models import Estoque
from funcionarios.models import Funcionario
from grupos_materiais.models import GrupoMaterial
from marcas.models import Marca
from materiais_papelaria.models import MaterialPapelaria


class AjusteEstoqueModelTest(TestCase):

    def setUp(self):
        self.grupo = GrupoMaterial.objects.create(
            nome='Material escolar',
            segmento='Escolar',
        )

        self.marca = Marca.objects.create(
            nome='Marca Teste',
            descricao='Marca utilizada nos testes',
            pais_origem='Brasil',
        )

        imagem = BytesIO()
        Image.new('RGB', (10, 10), color='white').save(
            imagem,
            format='PNG',
        )

        self.material = MaterialPapelaria.objects.create(
            codigo_interno='MAT-TESTE-001',
            nome_comercial='Caderno de teste',
            preco_venda=Decimal('10.00'),
            imagem_material=SimpleUploadedFile(
                'teste.png',
                imagem.getvalue(),
                content_type='image/png',
            ),
            grupo=self.grupo,
            marca=self.marca,
        )

        self.funcionario = Funcionario.objects.create(
            nome='Funcionário Teste',
            cpf='000.000.000-00',
            cargo='Auxiliar',
            data_admissao=date(2025, 1, 1),
        )

        self.estoque = Estoque.objects.create(
            material=self.material,
            quantidade=10,
            estoque_minimo=2,
            localizacao='Prateleira A',
        )

    def tearDown(self):
        if self.material.imagem_material:
            self.material.imagem_material.delete(save=False)

    def criar_ajuste(self):
        ajuste = AjusteEstoque(
            material=self.material,
            funcionario=self.funcionario,
            quantidade_contada=15,
            motivo='Correção de inventário',
        )
        ajuste.registrar_ajuste()
        return ajuste

    def test_registrar_ajuste_atualiza_estoque(self):
        ajuste = self.criar_ajuste()

        self.estoque.refresh_from_db()
        ajuste.refresh_from_db()

        self.assertEqual(self.estoque.quantidade, 15)
        self.assertEqual(ajuste.quantidade_anterior, 10)
        self.assertEqual(ajuste.quantidade_contada, 15)
        self.assertEqual(ajuste.diferenca, 5)

    def test_nao_permite_alterar_ajuste_registrado(self):
        ajuste = self.criar_ajuste()

        ajuste.motivo = 'Tentativa de alteração'

        with self.assertRaises(ValidationError):
            ajuste.save()

    def test_nao_permite_excluir_ajuste_registrado(self):
        ajuste = self.criar_ajuste()

        with self.assertRaises(ValidationError):
            ajuste.delete()

        self.assertTrue(
            AjusteEstoque.objects.filter(pk=ajuste.pk).exists()
        )

    def test_nao_permite_alterar_ajuste_por_update(self):
        self.criar_ajuste()

        with self.assertRaises(ValidationError):
            AjusteEstoque.objects.all().update(
                motivo='Tentativa de alteração em lote'
            )

    def test_nao_permite_excluir_ajuste_por_queryset(self):
        self.criar_ajuste()

        with self.assertRaises(ValidationError):
            AjusteEstoque.objects.all().delete()

    def test_nao_permite_criar_ajuste_por_bulk_create(self):
        ajuste = AjusteEstoque(
            material=self.material,
            funcionario=self.funcionario,
            quantidade_anterior=10,
            quantidade_contada=15,
            diferenca=5,
            motivo='Tentativa de criação em lote',
        )

        with self.assertRaises(ValidationError):
            AjusteEstoque.objects.bulk_create([ajuste])

    def test_nao_permite_registrar_ajuste_duas_vezes(self):
        ajuste = self.criar_ajuste()

        with self.assertRaises(ValidationError):
            ajuste.registrar_ajuste()
