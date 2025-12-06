<<<<<<< HEAD
# appPedidos/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import PedidoViewSet, estadisticas_tiempos

# Router para los endpoints del ViewSet
=======
from django.urls import path, include
from rest_framework import routers
from .views import PedidoViewSet

>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
router = routers.DefaultRouter()
router.register(r'pedidos', PedidoViewSet, basename='pedido')

urlpatterns = [
<<<<<<< HEAD
    # Endpoints generados automáticamente por el ViewSet
    path('', include(router.urls)),

    # Endpoint de estadísticas
    path('estadisticas/tiempos/', estadisticas_tiempos, name='estadisticas-tiempos'),
=======
    path('', include(router.urls)),
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
]
