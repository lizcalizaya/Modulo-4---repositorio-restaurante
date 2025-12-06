from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
<<<<<<< HEAD
from rest_framework import status
from django.db.models import Avg, Min, Max, F, ExpressionWrapper, DurationField
from drf_spectacular.utils import extend_schema
from .models import Pedido
# Django
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q, Avg, Min, Max, F, ExpressionWrapper, DurationField
from django import forms

# Django REST Framework
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

# drf-spectacular
from drf_spectacular.utils import extend_schema

# Tu app
from .models import Pedido
from .serializers import PedidoSerializer

=======
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Pedido
from .serializers import PedidoSerializer
from django.shortcuts import render
from django.db.models import Q
from django import forms
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836

def monitor(request):
    return render(request, 'monitor.html')

<<<<<<< HEAD
class PedidoViewSet(viewsets.ModelViewSet):
=======

class PedidoViewSet(viewsets.ModelViewSet):
    # Ocultar ENTREGADOS en la pantalla principal
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
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

<<<<<<< HEAD
        if nuevo_estado is None:
            return super().update(request, *args, **kwargs)

=======
        # Si solo actualiza mesa, cliente o descripcion:
        if nuevo_estado is None:
            return super().update(request, *args, **kwargs)

        # Si intenta cambiar estado
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
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

<<<<<<< HEAD

# ---------------- DETALLE PEDIDO ----------------
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    ahora = timezone.now()

=======
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)

    ahora = timezone.now()

    # Si el pedido está ENTREGADO, tomamos fecha_actualizacion como hora de salida
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
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

<<<<<<< HEAD

# ---------------- ADMINISTRAR PEDIDOS ----------------
def administrar_pedidos(request):
=======
def administrar_pedidos(request):
    # Eliminar pedido (POST)
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
    if request.method == "POST":
        eliminar_id = request.POST.get("eliminar_id")
        if eliminar_id:
            Pedido.objects.filter(pk=eliminar_id).delete()
            return redirect("administrar_pedidos")

<<<<<<< HEAD
=======
    # Búsqueda (GET)
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
    consulta = request.GET.get("q", "").strip()
    pedidos = Pedido.objects.all().order_by("-fecha_creacion")

    if consulta:
<<<<<<< HEAD
=======
        # Buscar por id (numérico), nombre de cliente o número de pedido (id)
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
        filtro = Q(cliente__icontains=consulta) | Q(descripcion__icontains=consulta)
        if consulta.isdigit():
            filtro |= Q(id=int(consulta))
        pedidos = pedidos.filter(filtro)
    else:
<<<<<<< HEAD
        pedidos = pedidos[:10]

    contexto = {"pedidos": pedidos, "consulta": consulta}
    return render(request, "administrar_pedidos.html", contexto)


# ---------------- FORMULARIO ----------------
=======
        # Si no hay búsqueda, mostrar los más recientes (por ejemplo 10)
        pedidos = pedidos[:10]

    contexto = {
        "pedidos": pedidos,
        "consulta": consulta,
    }
    return render(request, "administrar_pedidos.html", contexto)


>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
class FormPedido(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["mesa", "cliente", "descripcion", "estado"]
<<<<<<< HEAD
        widgets = {"descripcion": forms.Textarea(attrs={"rows": 3})}


# ---------------- EDITAR PEDIDO ----------------
=======
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }

>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)

    if request.method == "POST":
        formulario = FormPedido(request.POST, instance=pedido)
        if formulario.is_valid():
            formulario.save()
            return redirect("administrar_pedidos")
    else:
        formulario = FormPedido(instance=pedido)

<<<<<<< HEAD
    contexto = {"pedido": pedido, "formulario": formulario}
    return render(request, "editar_pedido.html", contexto)


# ---------------- HISTORIAL ----------------
def historial_pedidos(request):
    hoy = timezone.localdate()
    pedidos = Pedido.objects.filter(fecha_creacion__date=hoy).order_by('fecha_creacion')
=======
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
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836

    registros = []
    for p in pedidos:
        hora_ingreso = p.fecha_creacion
<<<<<<< HEAD
        hora_salida = p.fecha_actualizacion if p.estado == Pedido.EstadoPedido.ENTREGADO else None
=======
        # Consideramos hora de salida cuando está ENTREGADO
        hora_salida = (
            p.fecha_actualizacion
            if p.estado == Pedido.EstadoPedido.ENTREGADO
            else None
        )
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
        registros.append({
            "pedido": p,
            "hora_ingreso": hora_ingreso,
            "hora_salida": hora_salida,
        })
<<<<<<< HEAD

    contexto = {"registros": registros}
    return render(request, "historial_pedidos.html", contexto)

@extend_schema(
    summary="Estadísticas de tiempos de preparación",
    description="Calcula promedio, mínimo, máximo y cantidad de pedidos LISTO.",
    responses={
        200: {
            "type": "object",
            "properties": {
                "promedio_minutos": {"type": "number"},
                "minimo_minutos": {"type": "number"},
                "maximo_minutos": {"type": "number"},
                "cantidad_pedidos": {"type": "integer"},
            },
            "example": {
                "promedio_minutos": 12.5,
                "minimo_minutos": 8.0,
                "maximo_minutos": 20.0,
                "cantidad_pedidos": 5
            }
        }
    }
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
=======
    contexto = {"registros": registros}
    return render(request, "historial_pedidos.html", contexto)
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
