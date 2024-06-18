from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from dashboards.models import Marca, Categoria, Producto, ProductoImagen, Cliente, Cupon, Orden, DetalleOrden, Carrito, DetalleCarrito, Review
from .serializers import MarcaSerializer, CategoriaSerializer, ProductoSerializer, ProductoImagenSerializer, ClienteSerializer, CuponSerializer, OrdenSerializer, DetalleOrdenSerializer, CarritoSerializer, DetalleCarritoSerializer, ReviewSerializer
from django.shortcuts import get_object_or_404
from django.db import transaction
from decimal import Decimal

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('query', None)
        if query:
            productos = Producto.objects.filter(nombre__icontains=query)
            serializer = ProductoSerializer(productos, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({"error": "No query parameter provided"}, status=400)

class ProductoImagenViewSet(viewsets.ModelViewSet):
    queryset = ProductoImagen.objects.all()
    serializer_class = ProductoImagenSerializer

class CuponViewSet(viewsets.ModelViewSet):
    queryset = Cupon.objects.all()
    serializer_class = CuponSerializer

    
from .serializers import DetalleOrdenProductoSerializer, OrdenProductoSerializer

class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return OrdenProductoSerializer
        return super().get_serializer_class()
    
class DetalleOrdenViewSet(viewsets.ModelViewSet):
    queryset = DetalleOrden.objects.all()
    serializer_class = DetalleOrdenSerializer
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return DetalleOrdenProductoSerializer
        return super().get_serializer_class()
    
#CARRITO
class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer
    
    @action(detail=False, methods=['post'])
    def crear_carrito(self, request):
        cliente_id = request.data.get('cliente')

        # Crear el carrito para el cliente
        carrito = Carrito.objects.create(cliente_id=cliente_id)

        serializer = CarritoSerializer(carrito)
                
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'], url_path='eliminar-carritos')
    def eliminar_carritos_por_cliente(self, request):
        cliente_id = request.data.get('cliente')
        if not cliente_id:
            return Response({"error": "El ID del cliente es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        carritos = Carrito.objects.filter(cliente_id=cliente_id)
        if not carritos.exists():
            return Response({"error": "No se encontraron carritos para el cliente especificado."}, status=status.HTTP_404_NOT_FOUND)

        carritos.delete()
        return Response({"message": "Todos los carritos asociados al cliente han sido eliminados."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['delete'])
    def eliminar_carrito(self, request, pk=None):
        carrito = self.get_object()
        carrito.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['put'])
    def marcar_como_pagado(self, request, pk=None):
        carrito = self.get_object()
        
        if carrito.pagado:
            return Response({"error": "El carrito ya ha sido marcado como pagado."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Marcar el carrito como pagado
        carrito.pagado = True
        carrito.save()
        
        # Crear una orden para este carrito y asociarla al cliente
        with transaction.atomic():
            orden = Orden.objects.create(cliente=carrito.cliente, total='0.0')  # Inicializar total como string
            
            # Transferir detalles del carrito a detalles de orden
            for detalle_carrito in carrito.detalles.all():
                # Convertir precio_unitario de string a Decimal
                precio_unitario = Decimal(detalle_carrito.precio_unitario)
                
                DetalleOrden.objects.create(
                    orden=orden,
                    producto=detalle_carrito.producto,
                    cantidad=detalle_carrito.cantidad,
                    precio_unitario=precio_unitario
                )
                
                # Actualizar el total de la orden
                orden.total = str(Decimal(orden.total) + detalle_carrito.cantidad * precio_unitario)
            
            orden.save()
        # Eliminar el carrito una vez que se ha convertido en orden
        carrito.delete()
        
        return Response({
            "message": f"El carrito {carrito.id} ha sido marcado como pagado y se ha creado la orden {orden.id} asociada.",
            "orden_id": orden.id
        }, status=status.HTTP_200_OK)
    
from .serializers import DetalleCarritoNameSerializer

class DetalleCarritoViewSet(viewsets.ModelViewSet):
    queryset = DetalleCarrito.objects.all()
    serializer_class = DetalleCarritoSerializer
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return DetalleCarritoNameSerializer
        return super().get_serializer_class()
    
    @action(detail=False, methods=['post'])
    def agregar_producto_al_carrito(self, request):
        carrito_id = request.data.get('carrito')
        producto_id = request.data.get('producto')
        cantidad = request.data.get('cantidad')
        precio_unitario = request.data.get('precio_unitario')  # Opcional: manejo de precio unitario

        # Validar que carrito_id y producto_id existen y el producto está disponible
        carrito = get_object_or_404(Carrito, pk=carrito_id)
        producto = get_object_or_404(Producto, pk=producto_id)

        # Crear el detalle del carrito
        detalle_carrito = DetalleCarrito.objects.create(
            carrito=carrito,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario if precio_unitario else producto.precio  # Usar precio del producto si no se proporciona precio_unitario
        )

        serializer = DetalleCarritoSerializer(detalle_carrito)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['delete'])
    def eliminar_producto_del_carrito(self, request, pk=None):
        detalle_carrito = self.get_object()
        detalle_carrito.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

from django.contrib.auth.hashers import check_password
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from dashboards.models import Cliente
from .serializers import ClienteSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
        
    @action(detail=False, methods=['post'])
    def register(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "El nombre de usuario y la contraseña son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

        user = Cliente.objects.create_user(username=username, password=password)
        serializer = ClienteSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "El nombre de usuario y la contraseña son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Cliente.objects.get(username=username)
        except Cliente.DoesNotExist:
            return Response({"error": "Credenciales inválidas."}, status=status.HTTP_401_UNAUTHORIZED)
        
        if check_password(password, user.password):
            refresh = RefreshToken.for_user(user)
            serializer = ClienteSerializer(user)
            return Response({
                "message": "Inicio de sesión exitoso.",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Credenciales inválidas."}, status=status.HTTP_401_UNAUTHORIZED)