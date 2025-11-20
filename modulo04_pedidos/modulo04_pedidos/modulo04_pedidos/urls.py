from django.contrib import admin
from django.urls import path, include
from appPedidos.views import monitor

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('appPedidos.urls')),  # API DRF
    path('monitor/', monitor, name='monitor'),
]
