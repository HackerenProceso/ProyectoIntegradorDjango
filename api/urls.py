from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MarcaViewSet, CategoriaViewSet, ProductoViewSet, ProductoImagenViewSet, ClienteViewSet, CuponViewSet, OrdenViewSet, DetalleOrdenViewSet, CarritoViewSet, DetalleCarritoViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'marcas', MarcaViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'producto-imagenes', ProductoImagenViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'cupones', CuponViewSet)
router.register(r'ordenes', OrdenViewSet)
router.register(r'detalles-orden', DetalleOrdenViewSet)
router.register(r'carritos', CarritoViewSet)
router.register(r'detalles-carrito', DetalleCarritoViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('productos/search/', ProductoViewSet.as_view({'get': 'search'}), name='producto-search'),
    path('clientes/login/', ClienteViewSet.as_view({'post': 'login'}), name='cliente-login'),
    path('clientes/register/', ClienteViewSet.as_view({'post': 'register'}), name='cliente-register'),
]