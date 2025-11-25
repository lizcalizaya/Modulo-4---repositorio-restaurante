from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Pedido
from .serializers import PedidoSerializer
from django.shortcuts import render
from django.db.models import Q
from django import forms

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

def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)

    ahora = timezone.now()

    # Si el pedido está ENTREGADO, tomamos fecha_actualizacion como hora de salida
    if pedido.estado == Pedido.EstadoPedido.ENTREGADO:
        hora_salida = pedido.fecha_actualizacion
        delta = pedido.fecha_actualizacion - pedido.fecha_creacion
    else:
        hora_salida = None
        delta = ahora - pedido.fecha_creacion

    total_segundos = int(delta.total_seconds())
    minutos = total_segundos // 60
    segundos = total_segundos % 60
    tiempo_en_cocina = f"{minutos} min {segundos} s"

    context = {
        "pedido": pedido,
        "tiempo_en_cocina": tiempo_en_cocina,
        "hora_salida": hora_salida,
    }
    return render(request, "detalle_pedido.html", context)

def administrar_pedidos(request):
    # Eliminar pedido (POST)
    if request.method == "POST":
        eliminar_id = request.POST.get("eliminar_id")
        if eliminar_id:
            Pedido.objects.filter(pk=eliminar_id).delete()
            return redirect("administrar_pedidos")

    # Búsqueda (GET)
    consulta = request.GET.get("q", "").strip()
    pedidos = Pedido.objects.all().order_by("-fecha_creacion")

    if consulta:
        # Buscar por id (numérico), nombre de cliente o número de pedido (id)
        filtro = Q(cliente__icontains=consulta) | Q(descripcion__icontains=consulta)
        if consulta.isdigit():
            filtro |= Q(id=int(consulta))
        pedidos = pedidos.filter(filtro)
    else:
        # Si no hay búsqueda, mostrar los más recientes (por ejemplo 10)
        pedidos = pedidos[:10]

    contexto = {
        "pedidos": pedidos,
        "consulta": consulta,
    }
    return render(request, "administrar_pedidos.html", contexto)


class FormPedido(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["mesa", "cliente", "descripcion", "estado"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }

def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)

    if request.method == "POST":
        formulario = FormPedido(request.POST, instance=pedido)
        if formulario.is_valid():
            formulario.save()
            return redirect("administrar_pedidos")
    else:
        formulario = FormPedido(instance=pedido)

    contexto = {
        "pedido": pedido,
        "formulario": formulario,
    }
    return render(request, "editar_pedido.html", contexto)

def historial_pedidos(request):
    """
    Historial de la jornada:
    - Hora de ingreso
    - Hora de salida
    - Tiempo total
    """
    hoy = timezone.localdate()
    pedidos = Pedido.objects.filter(
        fecha_creacion__date=hoy
    ).order_by('fecha_creacion')

    registros = []
    for p in pedidos:
        hora_ingreso = p.fecha_creacion
        # Consideramos hora de salida cuando está ENTREGADO
        hora_salida = (
            p.fecha_actualizacion
            if p.estado == Pedido.EstadoPedido.ENTREGADO
            else None
        )
        registros.append({
            "pedido": p,
            "hora_ingreso": hora_ingreso,
            "hora_salida": hora_salida,
        })

    contexto = {"registros": registros}
    return render(request, "historial_pedidos.html", contexto)