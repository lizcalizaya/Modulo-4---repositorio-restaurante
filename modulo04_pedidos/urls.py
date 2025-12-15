from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from appPedidos.views import (
    monitor,
    detalle_pedido,
    administrar_pedidos,
    editar_pedido,
    historial_pedidos
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Página inicio -> monitor
    path('', monitor, name='monitor'),

    # API: usa solo el router de appPedidos
    path('api/', include('appPedidos.urls')),  

    # Monitor y detalle
    path('monitor/', monitor, name='monitor'),
    path('monitor/pedido/<int:pedido_id>/', detalle_pedido, name='detalle_pedido'),

    # Administración
    path('administrar-pedidos/', administrar_pedidos, name='administrar_pedidos'),
    path('administrar-pedidos/editar/<int:pedido_id>/', editar_pedido, name='editar_pedido'),

    # Historial
    path('historial/', historial_pedidos, name='historial_pedidos'),

    # Swagger y Redoc
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

