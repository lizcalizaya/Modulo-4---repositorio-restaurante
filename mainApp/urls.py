from django.urls import path, include
from rest_framework import routers
from .views import PedidoViewSet, monitor

router = routers.DefaultRouter()
router.register(r'pedidos', PedidoViewSet, basename='pedido')

urlpatterns = [
    # FRONTEND monitor
    path('monitor/', monitor, name='monitor'),

    # API REST generada por el router
    path('', include(router.urls)),
]
