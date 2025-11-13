from django.test import TestCase
from .models import Pedido

class PedidoModelTest(TestCase):
    def test_crear_pedido_default_estado(self):
        p = Pedido.objects.create(cliente='Test')
        self.assertEqual(p.estado, Pedido.EstadoPedido.CREADO)
