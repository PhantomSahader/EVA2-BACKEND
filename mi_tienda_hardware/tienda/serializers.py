from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Categoria, Producto, Carro, ItemCarro, Orden, DetalleOrden

# Serializador JWT personalizado para inyectar el rol de Administrador (is_staff)
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_staff'] = user.is_staff
        token['username'] = user.username
        return token

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')

    class Meta:
        model = Producto
        fields = '__all__'

class ItemCarroSerializer(serializers.ModelSerializer):
    producto_detalle = ProductoSerializer(source='producto', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItemCarro
        fields = ['id', 'producto', 'producto_detalle', 'cantidad', 'subtotal']

    def get_subtotal(self, obj):
        return obj.cantidad * obj.producto.precio

class CarroSerializer(serializers.ModelSerializer):
    items = ItemCarroSerializer(many=True, read_only=True)
    total_carro = serializers.SerializerMethodField()

    class Meta:
        model = Carro
        fields = ['id', 'usuario', 'items', 'total_carro', 'actualizado_en']

    def get_total_carro(self, obj):
        return sum(item.cantidad * item.producto.precio for item in obj.items.all())

class DetalleOrdenSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')

    class Meta:
        model = DetalleOrden
        fields = ['id', 'producto', 'producto_nombre', 'cantidad', 'precio_unitario']

class OrdenSerializer(serializers.ModelSerializer):
    detalles = DetalleOrdenSerializer(many=True, read_only=True)

    class Meta:
        model = Orden
        fields = ['id', 'usuario', 'fecha_creacion', 'estado', 'total', 'detalles']