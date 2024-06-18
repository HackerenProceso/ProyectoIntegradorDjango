from rest_framework import serializers
from dashboards.models import Marca, Categoria, Producto, ProductoImagen, Cliente, Cupon, Orden, DetalleOrden, Carrito, DetalleCarrito, Review

class ProductoImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoImagen
        fields = '__all__'
        
    def get_imagen(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.imagen.url)
        return obj.imagen.url

# Mostrar Info detallada
class ALLCategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'
        
class ALLMarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
                                
class SimpleProductoSerializer(serializers.ModelSerializer):
    categoria = ALLCategoriaSerializer()
    marca = ALLMarcaSerializer()
    imagenes = ProductoImagenSerializer(many=True, read_only=True)
    
    class Meta:
        model = Producto
        fields = '__all__'
        
# Categorias     
class CategoriaSerializer(serializers.ModelSerializer):
    productos = SimpleProductoSerializer(many=True, read_only=True, source='producto_set')

    class Meta:
        model = Categoria
        fields = '__all__'
        
# Marca
class MarcaSerializer(serializers.ModelSerializer):
    productos = SimpleProductoSerializer(many=True, read_only=True, source='producto_set')
    
    class Meta:
        model = Marca
        fields = '__all__'  
         
# Mostrar Info detallada en Producto    
class PCategoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categoria
        fields = '__all__'
        
class PMarcaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Marca
        fields = '__all__'          
         
# Productos
class ProductoSerializer(serializers.ModelSerializer):
    categoria = PCategoriaSerializer()
    marca = PMarcaSerializer()
    imagenes = ProductoImagenSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Producto
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class CuponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cupon
        fields = '__all__'
#CARRITO
class DetalleCarritoNameSerializer(serializers.ModelSerializer):
    producto = serializers.StringRelatedField()  # Muestra el nombre del producto

    class Meta:
        model = DetalleCarrito
        fields = '__all__'
        
class DetalleCarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleCarrito
        fields = '__all__'

class CarritoSerializer(serializers.ModelSerializer):
    detalles = DetalleCarritoNameSerializer(many=True, read_only=True, source='detalles.all')

    class Meta:
        model = Carrito
        fields = 'id', 'cliente', 'detalles', 'pagado'
 
#ORDEN     
class DetalleOrdenProductoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()
    
    class Meta:
        model = DetalleOrden
        fields = '__all__'
        
class DetalleOrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleOrden
        fields = '__all__'

class OrdenProductoSerializer(serializers.ModelSerializer):
    detalles = DetalleOrdenProductoSerializer(many=True, read_only=True, source='detalles.all')

    class Meta:
        model = Orden
        fields = '__all__'
        
class OrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orden
        fields = '__all__'