from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from appPedidos.views import (
    monitor,
    detalle_pedido,
    administrar_pedidos,
    editar_pedido,
    PedidoViewSet
)
from appPedidos import views as pedidos_views

# ViewSet manuales
cola_cocina_view = PedidoViewSet.as_view({'get': 'list'})
pedido_estado_view = PedidoViewSet.as_view({'patch': 'update'})

urlpatterns = [
    path('admin/', admin.site.urls),

    # Página inicio -> monitor
    path('', monitor, name='monitor'),

    # API
    path('api/', include('appPedidos.urls')),  

    # Monitor y detalle
    path('monitor/', monitor, name='monitor'),
    path('monitor/pedido/<int:pedido_id>/', detalle_pedido, name='detalle_pedido'),

    # Administración
    path('administrar-pedidos/', administrar_pedidos, name='administrar_pedidos'),
    path('administrar-pedidos/editar/<int:pedido_id>/', editar_pedido, name='editar_pedido'),

    # Cocina
    path('cocina/cola/', cola_cocina_view, name='cocina_cola'),

    # Historial
    path('historial/', pedidos_views.historial_pedidos, name='historial_pedidos'),

    # Swagger y Redoc
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

    path('historial/', pedidos_views.historial_pedidos, name='historial_pedidos'),
]
=======
]
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
