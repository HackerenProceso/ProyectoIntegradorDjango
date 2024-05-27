from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class Perfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='uploads/clientes', blank=True)
    telefono = models.CharField(max_length=9)
    direccion = models.TextField()

    def __str__(self):
        return self.user.username + "'s Profile"
    
# Create your models here.
class Marca(models.Model):
    nombre = models.CharField(max_length=150)
    
    def __str__(self):
        return f"{self.id}: {self.nombre}"

class Categoria(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=250)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen_url = models.ImageField(upload_to='assets/uploads/clientes', blank=True)
    descripcion = models.TextField()
    stock = models.IntegerField()
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    lote = models.CharField(max_length=100)  

class Cupon(models.Model):
    codigo = models.CharField(max_length=8)
    descuento = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_expiracion = models.DateField(null=True, blank=True)
    usado_por = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.codigo

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    username = models.CharField(max_length=150, unique=True)
    contraseña = models.CharField(max_length=128)
    imagen = models.ImageField(upload_to='assets/uploads/clientes', blank=True)
    telefono = models.CharField(max_length=9)
    direccion = models.TextField()
    fecha_de_registro = models.DateTimeField(default=timezone.now)
    ultimo_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username + "'s Profile"
    
class Orden(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ordenes')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Orden de {self.cliente.username} - {self.fecha}"

class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

class Carrito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='carritos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    orden_asociada = models.OneToOneField(Orden, on_delete=models.CASCADE, null=True, blank=True, related_name='carrito_asociado')

    def __str__(self):
        return f"Carrito de {self.cliente.username} - {self.fecha_creacion}"

class DetalleCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)