from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Pedido
from .serializers import PedidoSerializer
from django.shortcuts import render

def monitor(request):
    return render(request, 'monitor.html')


class PedidoViewSet(viewsets.ModelViewSet):
    # Ocultar ENTREGADOS en la pantalla principal
    queryset = Pedido.objects.all().order_by('-fecha_creacion')
    serializer_class = PedidoSerializer

    # Transiciones válidas
    transiciones = {
        "URGENTE": ["EN_PREPARACION"],
        "CREADO": ["URGENTE", "EN_PREPARACION"],
        "EN_PREPARACION": ["LISTO"],
        "LISTO": ["ENTREGADO"],
        "ENTREGADO": []
    }

    # ---- UPDATE ----
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        nuevo_estado = request.data.get("estado", None)

        # Si solo actualiza mesa, cliente o descripcion:
        if nuevo_estado is None:
            return super().update(request, *args, **kwargs)

        # Si intenta cambiar estado
        if nuevo_estado not in self.transiciones[instance.estado]:
            return Response(
                {"error": f"No puedes pasar de {instance.estado} a {nuevo_estado}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.estado = nuevo_estado
        instance.save()
        return Response(PedidoSerializer(instance).data)

    # -------- FILTRO POR ESTADO --------
    @action(detail=False, methods=['get'])
    def filtrados(self, request):
        estado = request.query_params.get('estado', 'CREADO').upper()
        pedidos = Pedido.objects.filter(estado=estado)
        return Response({
            "estado": estado,
            "cantidad": pedidos.count(),
            "resultados": PedidoSerializer(pedidos, many=True).data
        })

    # -------- SOLO ENTREGADOS --------
    @action(detail=False, methods=['get'])
    def entregados(self, request):
        pedidos = Pedido.objects.filter(estado="ENTREGADO")
        return Response(PedidoSerializer(pedidos, many=True).data)

