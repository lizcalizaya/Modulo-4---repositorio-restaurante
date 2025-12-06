<<<<<<< HEAD
from django.contrib import admin
from django.urls import path, include
from appPedidos.views import monitor

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('appPedidos.urls')),  # API DRF
    path('monitor/', monitor, name='monitor'),
]
=======
from django.contrib import admin
from django.urls import path, include
from appPedidos.views import monitor

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('appPedidos.urls')),  # API DRF
    path('monitor/', monitor, name='monitor'),
]
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
