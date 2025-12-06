<<<<<<< HEAD
from django.urls import path, include
from rest_framework import routers
from .views import PedidoViewSet

router = routers.DefaultRouter()
router.register(r'pedidos', PedidoViewSet, basename='pedido')

urlpatterns = [
    path('', include(router.urls)),
]
=======
from django.urls import path, include
from rest_framework import routers
from .views import PedidoViewSet

router = routers.DefaultRouter()
router.register(r'pedidos', PedidoViewSet, basename='pedido')

urlpatterns = [
    path('', include(router.urls)),
]
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
