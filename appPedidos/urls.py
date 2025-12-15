# appPedidos/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import PedidoViewSet, estadisticas_tiempos, debug_db


router = routers.DefaultRouter()
router.register(r'pedidos', PedidoViewSet, basename='pedido')

urlpatterns = [
    # Endpoints del ViewSet
    path('', include(router.urls)),
    path("debug-db/", debug_db),


    # Endpoint de estadísticas
    path('estadisticas/tiempos/', estadisticas_tiempos, name='estadisticas-tiempos'),
]

