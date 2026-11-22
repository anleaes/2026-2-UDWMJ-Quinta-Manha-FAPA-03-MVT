from django.db import models


class MaterialPapelaria(models.Model):
    codigo_interno = models.CharField('Código Interno', max_length=50)
    nome_comercial = models.CharField('Nome Comercial', max_length=100)
    preco_venda = models.DecimalField('Preço de Venda', max_digits=10, decimal_places=2)
    imagem_material = models.ImageField(
        'Imagem do Material',
        upload_to='materiais/',
    )
    grupo = models.ForeignKey(
        'grupos_materiais.GrupoMaterial',
        on_delete=models.PROTECT,
        related_name='materiais',
        verbose_name='Grupo',
    )
    marca = models.ForeignKey(
        'marcas.Marca',
        on_delete=models.PROTECT,
        related_name='materiais',
        verbose_name='Marca',
    )
    ativo = models.BooleanField('Ativo', default=True)

    def alterar_preco(self, novo_preco):
        self.preco_venda = novo_preco
        self.full_clean()
        self.save()

    def ativar(self):
        self.ativo = True
        self.save()

    def desativar(self):
        self.ativo = False
        self.save()

    class Meta:
        verbose_name = 'Material de Papelaria'
        verbose_name_plural = 'Materiais de Papelaria'
        ordering = ['nome_comercial']

    def __str__(self):
        return self.nome_comercial
