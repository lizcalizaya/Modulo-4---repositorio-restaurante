from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q, Avg, Min, Max, F, ExpressionWrapper, DurationField
from django import forms
from django.http import JsonResponse
from django.db import connection


from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from .models import Pedido
from .serializers import PedidoSerializer
import requests
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def debug_db(request):
    return Response({
        "total_pedidos": Pedido.objects.count()
    })


def monitor(request):
    return render(request, 'monitor.html')


def notificar_modulo3_listo(pedido: Pedido):
    url = settings.MODULO3_API_BASE.rstrip("/") + settings.MODULO3_LISTO_ENDPOINT

    payload = {
        "id_pedido": pedido.id_modulo3 or pedido.id,
        "numero_mesa": pedido.mesa,
        "nombre_cliente": pedido.cliente,
        "orden": pedido.descripcion,
        "hora_salida": pedido.hora_listo.isoformat() if pedido.hora_listo else None,
        "estado": pedido.estado,
    }

    # timeout para que no se “cuelgue” tu API
    r = requests.post(url, json=payload, timeout=5)
    r.raise_for_status()
class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all().order_by("-fecha_creacion")
    serializer_class = PedidoSerializer

    transiciones = {
        "URGENTE": ["EN_PREPARACION"],
        "CREADO": ["URGENTE", "EN_PREPARACION"],
        "EN_PREPARACION": ["LISTO"],
        "LISTO": ["ENTREGADO"],
        "ENTREGADO": []
    }

    # 🔹 LIST seguro
    def list(self, request, *args, **kwargs):
        """
        GET /api/pedidos/
        Devuelve todos los pedidos sin tocar estados ni transiciones.
        """
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            print("ERROR EN LIST():", e)
            return Response(
                {"error": "Ocurrió un error al listar pedidos."},
                status=500
            )

    # 🔹 UPDATE seguro
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        nuevo_estado = request.data.get("estado", None)

        if nuevo_estado is None:
            return super().update(request, *args, **kwargs)

        if nuevo_estado not in self.transiciones[instance.estado]:
            return Response(
                {"error": f"No puedes pasar de {instance.estado} a {nuevo_estado}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.estado = nuevo_estado

        # Si pasa a LISTO, guardamos hora_listo 1 sola vez
        if nuevo_estado == "LISTO" and instance.hora_listo is None:
            instance.hora_listo = timezone.now()

        instance.save()

        # Notificación a módulo 03 eliminada temporalmente
        # Para evitar dependencias externas y errores en deploy

        return Response(PedidoSerializer(instance).data)

    # 🔹 Filtrados por estado
    @action(detail=False, methods=['get'])
    def filtrados(self, request):
        estado = request.query_params.get('estado', 'CREADO').upper()
        pedidos = Pedido.objects.filter(estado=estado)
        return Response({
            "estado": estado,
            "cantidad": pedidos.count(),
            "resultados": PedidoSerializer(pedidos, many=True).data
        })

    # 🔹 Pedidos entregados
    @action(detail=False, methods=['get'])
    def entregados(self, request):
        pedidos = Pedido.objects.filter(estado="ENTREGADO")
        return Response(PedidoSerializer(pedidos, many=True).data)

    # 🔹 Crear/actualizar desde módulo 03
    @action(detail=False, methods=["post"], url_path="desde-modulo3")
    def desde_modulo3(self, request):
        id_pedido = request.data.get("id_pedido")
        nro_mesa = request.data.get("nro_mesa")
        nombre_cliente = request.data.get("nombre_cliente")
        orden = request.data.get("orden")

        if id_pedido is None or nro_mesa is None or not nombre_cliente or orden is None:
            return Response(
                {"error": "Faltan campos. Requeridos: id_pedido, nro_mesa, nombre_cliente, orden"},
                status=status.HTTP_400_BAD_REQUEST
            )

        pedido, creado = Pedido.objects.get_or_create(
            id_modulo3=int(id_pedido),
            defaults={
                "mesa": int(nro_mesa),
                "cliente": str(nombre_cliente),
                "descripcion": str(orden),
                "estado": Pedido.EstadoPedido.CREADO,
            }
        )

        if not creado:
            pedido.mesa = int(nro_mesa)
            pedido.cliente = str(nombre_cliente)
            pedido.descripcion = str(orden)
            pedido.save()

        return Response(
            {"ok": True, "creado": creado, "pedido": PedidoSerializer(pedido).data},
            status=status.HTTP_201_CREATED if creado else status.HTTP_200_OK
        )


def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    ahora = timezone.now()

    if pedido.estado == Pedido.EstadoPedido.ENTREGADO:
        hora_salida = pedido.fecha_actualizacion
        delta = pedido.fecha_actualizacion - pedido.fecha_creacion
    else:
        hora_salida = None
        delta = ahora - pedido.fecha_creacion

    total_segundos = int(delta.total_seconds())
    minutos = total_segundos // 60
    segundos = total_segundos % 60

    context = {
        "pedido": pedido,
        "tiempo_en_cocina": f"{minutos} min {segundos} s",
        "hora_salida": hora_salida,
    }
    return render(request, "detalle_pedido.html", context)


def administrar_pedidos(request):
    if request.method == "POST":
        eliminar_id = request.POST.get("eliminar_id")
        if eliminar_id:
            Pedido.objects.filter(pk=eliminar_id).delete()
            return redirect("administrar_pedidos")

    consulta = request.GET.get("q", "").strip()
    pedidos = Pedido.objects.all().order_by("-fecha_creacion")

    if consulta:
        filtro = Q(cliente__icontains=consulta) | Q(descripcion__icontains=consulta)
        if consulta.isdigit():
            filtro |= Q(id=int(consulta))
        pedidos = pedidos.filter(filtro)
    else:
        pedidos = pedidos[:10]

    contexto = {"pedidos": pedidos, "consulta": consulta}
    return render(request, "administrar_pedidos.html", contexto)


class FormPedido(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["mesa", "cliente", "descripcion", "estado"]
        widgets = {"descripcion": forms.Textarea(attrs={"rows": 3})}


def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)

    if request.method == "POST":
        formulario = FormPedido(request.POST, instance=pedido)
        if formulario.is_valid():
            formulario.save()
            return redirect("administrar_pedidos")
    else:
        formulario = FormPedido(instance=pedido)

    contexto = {"pedido": pedido, "formulario": formulario}
    return render(request, "editar_pedido.html", contexto)


def historial_pedidos(request):
    hoy = timezone.localdate()
    pedidos = Pedido.objects.filter(fecha_creacion__date=hoy).order_by('fecha_creacion')

    registros = []
    for p in pedidos:
        hora_ingreso = p.fecha_creacion
        hora_salida = p.fecha_actualizacion if p.estado == Pedido.EstadoPedido.ENTREGADO else None
        registros.append({
            "pedido": p,
            "hora_ingreso": hora_ingreso,
            "hora_salida": hora_salida,
        })

    contexto = {"registros": registros}
    return render(request, "historial_pedidos.html", contexto)


@extend_schema(
    summary="Estadísticas de tiempos de preparación",
    description="Calcula promedio, mínimo, máximo y cantidad de pedidos LISTO.",
)
@api_view(["GET"])
def estadisticas_tiempos(request):
    pedidos = Pedido.objects.filter(estado="LISTO", fecha_actualizacion__isnull=False)

    if not pedidos.exists():
        return Response({
            "promedio_minutos": 0,
            "minimo_minutos": 0,
            "maximo_minutos": 0,
            "cantidad_pedidos": 0
        }, status=status.HTTP_200_OK)

    diff = ExpressionWrapper(
        F("fecha_actualizacion") - F("fecha_creacion"),
        output_field=DurationField()
    )

    datos = pedidos.aggregate(
        promedio=Avg(diff),
        minimo=Min(diff),
        maximo=Max(diff),
    )

    def to_minutes(td):
        return round(td.total_seconds() / 60, 2) if td else 0

    return Response({
        "promedio_minutos": to_minutes(datos["promedio"]),
        "minimo_minutos": to_minutes(datos["minimo"]),
        "maximo_minutos": to_minutes(datos["maximo"]),
        "cantidad_pedidos": pedidos.count(),
    }, status=status.HTTP_200_OK)

