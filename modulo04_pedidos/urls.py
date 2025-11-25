from django.contrib import admin
from django.urls import path, include
from appPedidos.views import monitor
from appPedidos.views import monitor, detalle_pedido
from appPedidos.views import monitor, detalle_pedido, administrar_pedidos, editar_pedido
from appPedidos.views import PedidoViewSet
from appPedidos import views as pedidos_views

cola_cocina_view = PedidoViewSet.as_view({'get': 'list'})
pedido_estado_view = PedidoViewSet.as_view({'patch': 'update'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('appPedidos.urls')),  # API DRF
    path('monitor/', monitor, name='monitor'),
    path('monitor/pedido/<int:pedido_id>/', detalle_pedido, name='detalle_pedido'),
    path('administrar-pedidos/', administrar_pedidos, name='administrar_pedidos'),
    path('administrar-pedidos/editar/<int:pedido_id>/', editar_pedido, name='editar_pedido'),
    path('cocina/cola/', cola_cocina_view, name='cocina_cola'),
    path('historial/', pedidos_views.historial_pedidos, name='historial_pedidos'),
]
