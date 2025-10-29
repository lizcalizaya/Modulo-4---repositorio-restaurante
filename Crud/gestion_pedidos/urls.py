from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from mainApp.views import PedidoViewSet

router = routers.DefaultRouter()
router.register(r'pedidos', PedidoViewSet, basename='pedido')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
