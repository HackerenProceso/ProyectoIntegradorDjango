from django.contrib import admin
from .models import Perfil, Marca, Categoria, Producto, Cupon, Cliente, Orden, DetalleOrden, Carrito, DetalleCarrito

# Register your models here.
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre') 


admin.site.register(Perfil)
admin.site.register(Marca)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Cupon)
admin.site.register(Cliente)
admin.site.register(Orden)
admin.site.register(DetalleOrden)
admin.site.register(Carrito)
admin.site.register(DetalleCarrito)
