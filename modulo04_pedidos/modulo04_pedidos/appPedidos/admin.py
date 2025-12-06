<<<<<<< HEAD
from django.contrib import admin
from .models import Pedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'estado', 'fecha_creacion', 'fecha_actualizacion')
    list_filter = ('estado',)
    search_fields = ('cliente',)
=======
from django.contrib import admin
from .models import Pedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'estado', 'fecha_creacion', 'fecha_actualizacion')
    list_filter = ('estado',)
    search_fields = ('cliente',)
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
