from rest_framework import viewsets, permissions
from dashboards.models import Cliente, Marca, Categoria, Producto, ProductoImagen, Cupon, Carrito, DetalleCarrito, Orden, DetalleOrden
from .serializers import ClienteSerializer, MarcaSerializer, CategoriaSerializer, ProductoSerializer, ProductoImagenSerializer, CuponSerializer, CarritoSerializer, DetalleCarritoSerializer, OrdenSerializer, DetalleOrdenSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.AllowAny]  # Permitir registro y login

class MarcaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoImagenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductoImagen.objects.all()
    serializer_class = ProductoImagenSerializer

class CuponViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cupon.objects.all()
    serializer_class = CuponSerializer

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)

class DetalleCarritoViewSet(viewsets.ModelViewSet):
    queryset = DetalleCarrito.objects.all()
    serializer_class = DetalleCarritoSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        carrito = Carrito.objects.get(cliente=self.request.user, orden_asociada__isnull=True)
        orden = serializer.save(cliente=self.request.user)
        carrito.orden_asociada = orden
        carrito.save()

class DetalleOrdenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DetalleOrden.objects.all()
    serializer_class = DetalleOrdenSerializer
    permission_classes = [permissions.IsAuthenticated]
