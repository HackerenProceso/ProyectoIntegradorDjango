from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.hashers import make_password

from django.db import models
# Create your models here.

class Perfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='uploads/clientes', blank=True)
    telefono = models.CharField(max_length=9)
    direccion = models.TextField()

    def __str__(self):
        return self.user.username + "'s Profile"
    
# Create your models here.
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.contrib.auth.hashers import make_password

class ClienteManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('El username es obligatorio')
        if not password:
            raise ValueError('El password es obligatorio')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Esta línea encripta la contraseña
        user.save(using=self._db)
        return user

class Cliente(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=30, blank=True, null=True)
    apellido = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)  # Hacerlo opcional
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)  # Agrega este campo para almacenar la contraseña
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='assets/uploads/clientes', blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='clientes', blank=True)  # Hacerlo opcional
    user_permissions = models.ManyToManyField(Permission, related_name='clientes', blank=True)  # Hacerlo opcional
    fecha_de_registro = models.DateTimeField(auto_now_add=True)  # Hacerlo opcional
    
    objects = ClienteManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


   
#Otros
class Marca(models.Model):
    nombre = models.CharField(max_length=150)
    imagen = models.ImageField(upload_to='assets/uploads/marcas')
    
    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='assets/uploads/categorias')
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=250)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    stock = models.IntegerField()
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    lote = models.CharField(max_length=100)  
    
    def __str__(self):
        return self.nombre

class ProductoImagen(models.Model):
    producto = models.ForeignKey(Producto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='assets/uploads/productos')

    def __str__(self):
        return f"Imagen for {self.producto.nombre}" 

class Cupon(models.Model):
    codigo = models.CharField(max_length=8)
    descuento = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_expiracion = models.DateField(null=True, blank=True)
    cliente_que_lo_uso = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name='cupones_utilizados')

    def __str__(self):
        return self.codigo    
    
class Review(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reviews')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='reviews')
    comentario = models.TextField()
    estrellas = models.PositiveIntegerField()

    def __str__(self):
        return f"Review by {self.cliente.username} for {self.producto.nombre} - {self.estrellas} estrellas"

    def save(self, *args, **kwargs):
        if self.estrellas < 1 or self.estrellas > 5:
            raise ValueError("Las estrellas deben estar entre 1 y 5")
        super().save(*args, **kwargs)
        
class Carrito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    pagado = models.BooleanField(default=False) 

    def __str__(self):
        return f"Carrito de {self.cliente.username}"

class Orden(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)  # Campo para almacenar el total de la orden

    def __str__(self):
        return f"Orden de {self.cliente.username} creada el {self.creado_en}"

class DetalleCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} en el carrito de {self.carrito.cliente.username}"

class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} en la orden de {self.orden.cliente.username}"