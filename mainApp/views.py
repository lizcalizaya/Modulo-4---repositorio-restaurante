from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Pedido
from .serializers import PedidoSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all().order_by('-fecha_creacion')
    serializer_class = PedidoSerializer

    # 🔹 Update con validación de transiciones de estado
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        nuevo_estado = request.data.get('estado')

        # si no se envía estado, proceder con update normal (otros campos)
        if nuevo_estado is None:
            return super().update(request, *args, **kwargs)

        transiciones_validas = {
            Pedido.EstadoPedido.CREADO: [Pedido.EstadoPedido.EN_PREPARACION],
            Pedido.EstadoPedido.EN_PREPARACION: [Pedido.EstadoPedido.LISTO],
            Pedido.EstadoPedido.LISTO: [Pedido.EstadoPedido.ENTREGADO],
            Pedido.EstadoPedido.ENTREGADO: []
        }

        if nuevo_estado not in transiciones_validas[instance.estado]:
            return Response(
                {'error': 'Transición de estado no válida'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # aplicar cambio de estado
        instance.estado = nuevo_estado
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # 🔹 Función auxiliar para los filtros por estado
    def _responder_por_estado(self, estado_nombre):
        pedidos = Pedido.objects.filter(estado=estado_nombre)
        serializer = self.get_serializer(pedidos, many=True)
        total = pedidos.count()
        return Response({
            "estado": estado_nombre,
            "cantidad": total,
            "mensaje": f"Hay {total} pedido(s) con estado '{estado_nombre}'",
            "resultados": serializer.data
        }, status=status.HTTP_200_OK)

    # 🟢 Endpoint: pedidos pendientes
    @action(detail=False, methods=['get'])
    def pendientes(self, request):
        return self._responder_por_estado('CREADO')

    # 🟡 Creados
    @action(detail=False, methods=['get'])
    def creados(self, request):
        return self._responder_por_estado('CREADO')

    # 🟠 En preparación
    @action(detail=False, methods=['get'])
    def en_preparacion(self, request):
        return self._responder_por_estado('EN_PREPARACION')

    # 🔵 Listos
    @action(detail=False, methods=['get'])
    def listos(self, request):
        return self._responder_por_estado('LISTO')

    # ⚪ Entregados
    @action(detail=False, methods=['get'])
    def entregados(self, request):
        return self._responder_por_estado('ENTREGADO')

    # 🚀 Extra: filtrado dinámico
    @action(detail=False, methods=['get'])
    def filtrados(self, request):
        estado = request.query_params.get('estado', 'CREADO').upper()
        return self._responder_por_estado(estado)


# 👇👇 ESTA ES LA VISTA DEL FRONTEND (MONITOR)
def monitor(request):
    """
    Renderiza la página del monitor de órdenes.
    monitor.html debe estar en la carpeta templates.
    """
    return render(request, "monitor.html")
