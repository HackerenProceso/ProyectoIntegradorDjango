from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from dashboards.models import Marca, Categoria, Producto, ProductoImagen, Cliente, Cupon, Orden, DetalleOrden, Carrito, DetalleCarrito, Review
from .serializers import MarcaSerializer, CategoriaSerializer, ProductoSerializer, ProductoImagenSerializer, ClienteSerializer, CuponSerializer, OrdenSerializer, DetalleOrdenSerializer, CarritoSerializer, DetalleCarritoSerializer, ReviewSerializer


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

class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer

class DetalleOrdenViewSet(viewsets.ModelViewSet):
    queryset = DetalleOrden.objects.all()
    serializer_class = DetalleOrdenSerializer

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

class DetalleCarritoViewSet(viewsets.ModelViewSet):
    queryset = DetalleCarrito.objects.all()
    serializer_class = DetalleCarritoSerializer

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
            return Response({
                "message": "Inicio de sesión exitoso.",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Credenciales inválidas."}, status=status.HTTP_401_UNAUTHORIZED)