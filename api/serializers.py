from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from dashboards.models import Cliente, Marca, Categoria, Producto, ProductoImagen, Cupon, Carrito, DetalleCarrito, Orden, DetalleOrden

class ClienteSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if password:
            validated_data['password'] = make_password(password)
        return super().create(validated_data)
    
    class Meta:
        model = Cliente
        fields = '__all__'
        
class MarcaSerializer(serializers.ModelSerializer):
    productos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Marca
        fields = '__all__'
        
class CategoriaSerializer(serializers.ModelSerializer):
    productos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Categoria
        fields = '__all__'
        
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'      

class ProductoImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoImagen
        fields = '__all__'  

class CuponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cupon
        fields = '__all__'

class CarritoSerializer(serializers.ModelSerializer):
    detalles = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Carrito
        fields = '__all__'        

class DetalleCarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleCarrito
        fields = '__all__'        

class OrdenSerializer(serializers.ModelSerializer):
    detalles = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Orden
        fields = '__all__'        

class DetalleOrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleOrden
        fields = '__all__'
