# modulo04_pedidos/urls.py

from django.contrib import admin
from django.urls import path, include
from appPedidos.views import monitor, detalle_pedido, administrar_pedidos, editar_pedido
from appPedidos.views import PedidoViewSet
from appPedidos import views as pedidos_views

cola_cocina_view = PedidoViewSet.as_view({'get': 'list'})
pedido_estado_view = PedidoViewSet.as_view({'patch': 'update'})

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. RUTA RAÍZ: La ruta vacía ('') ahora apunta a la vista 'monitor'.
    path('', monitor, name='monitor'), 
    
    # 2. RUTA API (sin cambios)
    path('api/', include('appPedidos.urls')),
    
    # 3. MANTENEMOS la ruta detallada del monitor (si se necesita)
    path('monitor/pedido/<int:pedido_id>/', detalle_pedido, name='detalle_pedido'),
    
    # 4. RESTO DE RUTAS (sin cambios)
    path('administrar-pedidos/', administrar_pedidos, name='administrar_pedidos'),
    path('administrar-pedidos/editar/<int:pedido_id>/', editar_pedido, name='editar_pedido'),
    path('cocina/cola/', cola_cocina_view, name='cocina_cola'),
    path('historial/', pedidos_views.historial_pedidos, name='historial_pedidos'),
]
