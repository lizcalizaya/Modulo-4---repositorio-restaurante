# appPedidos/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import PedidoViewSet, estadisticas_tiempos

# Router para los endpoints del ViewSet
router = routers.DefaultRouter()
router.register(r'pedidos', PedidoViewSet, basename='pedido')

urlpatterns = [
    # Endpoints generados automáticamente por el ViewSet
    path('', include(router.urls)),

    # Endpoint de estadísticas
    path('estadisticas/tiempos/', estadisticas_tiempos, name='estadisticas-tiempos'),
]
