<<<<<<< HEAD
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
=======
# modulo04_pedidos/urls.py

from django.contrib import admin
from django.urls import path, include
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
from appPedidos.views import monitor, detalle_pedido, administrar_pedidos, editar_pedido
from appPedidos.views import PedidoViewSet
from appPedidos import views as pedidos_views

<<<<<<< HEAD
# ViewSet manuales
=======
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
cola_cocina_view = PedidoViewSet.as_view({'get': 'list'})
pedido_estado_view = PedidoViewSet.as_view({'patch': 'update'})

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('api/', include('appPedidos.urls')),  # API DRF
    path('monitor/', monitor, name='monitor'),
    path('monitor/pedido/<int:pedido_id>/', detalle_pedido, name='detalle_pedido'),
=======
    
    # 1. RUTA RAÍZ: La ruta vacía ('') ahora apunta a la vista 'monitor'.
    path('', monitor, name='monitor'), 
    
    # 2. RUTA API (sin cambios)
    path('api/', include('appPedidos.urls')),
    
    # 3. MANTENEMOS la ruta detallada del monitor (si se necesita)
    path('monitor/pedido/<int:pedido_id>/', detalle_pedido, name='detalle_pedido'),
    
    # 4. RESTO DE RUTAS (sin cambios)
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
    path('administrar-pedidos/', administrar_pedidos, name='administrar_pedidos'),
    path('administrar-pedidos/editar/<int:pedido_id>/', editar_pedido, name='editar_pedido'),
    path('cocina/cola/', cola_cocina_view, name='cocina_cola'),
    path('historial/', pedidos_views.historial_pedidos, name='historial_pedidos'),
<<<<<<< HEAD

    #Swagger y Redoc
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    #Vsitas del HTML
    path('monitor/', monitor, name='monitor'),
    path('monitor/pedido/<int:pedido_id>/', detalle_pedido, name='detalle_pedido'),
    path('administrar-pedidos/', administrar_pedidos, name='administrar_pedidos'),
    path('administrar-pedidos/editar/<int:pedido_id>/', editar_pedido, name='editar_pedido'),
    path('cocina/cola/', cola_cocina_view, name='cocina_cola'),
    path('historial/', pedidos_views.historial_pedidos, name='historial_pedidos'),
]
=======
]
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
