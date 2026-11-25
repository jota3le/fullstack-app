from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Produto, Venda

class PDVServicosTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='operador', password='123')
        self.produto = Produto.objects.create(
            nome='Salgado Assado', categoria='Lanches', quantidade=10, preco=7.50
        )

    def test_autorizacao_rota_protegida(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

    def test_autenticacao_login(self):
        logged = self.client.login(username='operador', password='123')
        self.assertTrue(logged)

    def test_transacao_cadastro_produto(self):
        self.client.login(username='operador', password='123')
        self.client.post(reverse('home'), {
            'nome': 'Suco Natural', 'categoria': 'Bebidas', 'quantidade': 5, 'preco': '6.00'
        })
        self.assertTrue(Produto.objects.filter(nome='Suco Natural').exists())

    def test_transacao_venda_e_baixa_estoque(self):
        self.client.login(username='operador', password='123')
        self.client.get(reverse('vender_produto', args=[self.produto.id]))
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade, 9)
        self.assertEqual(Venda.objects.count(), 1)

    def test_transacao_repor_estoque(self):
        self.client.login(username='operador', password='123')
        self.client.get(reverse('repor_estoque', args=[self.produto.id]))
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade, 11)

    def test_transacao_excluir_produto(self):
        self.client.login(username='operador', password='123')
        self.client.get(reverse('deletar_produto', args=[self.produto.id]))
        self.assertFalse(Produto.objects.filter(id=self.produto.id).exists())