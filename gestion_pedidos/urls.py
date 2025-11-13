from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('mainApp.urls')),   # todas las rutas de mainApp debajo de /api/
]
