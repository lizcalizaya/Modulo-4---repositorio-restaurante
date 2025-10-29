from django.db import models

class Pedido(models.Model):
    class EstadoPedido(models.TextChoices):
        CREADO = 'CREADO', 'Creado'
        EN_PREPARACION = 'EN_PREPARACION', 'En preparación'
        LISTO = 'LISTO', 'Listo'
        ENTREGADO = 'ENTREGADO', 'Entregado'

    cliente = models.CharField(max_length=100)
    estado = models.CharField(
        max_length=20,
        choices=EstadoPedido.choices,
        default=EstadoPedido.CREADO
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.get_estado_display()}"
