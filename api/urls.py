# urls.py
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api import views

router = routers.DefaultRouter()
router.register(r'clientes', views.ClienteViewSet)
router.register(r'marcas', views.MarcaViewSet)
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'productos', views.ProductoViewSet)
router.register(r'imagenesProductos', views.ProductoImagenViewSet)
router.register(r'cupones', views.CuponViewSet)
router.register(r'carritos', views.CarritoViewSet)
router.register(r'detalleCarritos', views.DetalleCarritoViewSet)
router.register(r'ordenes', views.OrdenViewSet)
router.register(r'detallesOrdenes', views.DetalleOrdenViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
