from django.urls import path, include
from rest_framework import routers
from .views import PedidoViewSet, estadisticas_tiempos

router = routers.DefaultRouter()
router.register(r'pedidos', PedidoViewSet, basename='pedido')

urlpatterns = [
    path('', include(router.urls)),
    path('estadisticas/tiempos/', estadisticas_tiempos, name='estadisticas-tiempos'),
]
