<<<<<<< HEAD
from rest_framework import serializers 
from .models import Pedido

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
=======
from rest_framework import serializers 
from .models import Pedido

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
