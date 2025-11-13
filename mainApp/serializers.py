from rest_framework import serializers
from .models import Pedido


class PedidoSerializer(serializers.ModelSerializer):
    # mesa ↔ cliente
    mesa = serializers.CharField(source='cliente')

    # estos son de solo lectura
    hora = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()
    detalles = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        # 👇 AHORA incluimos 'descripcion' como campo normal
        fields = ['id', 'mesa', 'descripcion', 'hora', 'estado', 'detalles']

    def get_hora(self, obj):
        if obj.fecha_creacion:
            return obj.fecha_creacion.strftime("%H:%M")
        return ""

    def get_estado(self, obj):
        return obj.get_estado_display()

    def get_detalles(self, obj):
        """
        Convierte la descripción en una lista de líneas.
        Ejemplo:
          "Menú 1 (1)\nBebestible: Fanta (1)"
        → ["Menú 1 (1)", "Bebestible: Fanta (1)"]
        """
        if not obj.descripcion:
            return []
        lineas = [l.strip() for l in obj.descripcion.split('\n') if l.strip()]
        return lineas
