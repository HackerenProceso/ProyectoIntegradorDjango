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
    
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.hashers import make_password

class ClienteManager(BaseUserManager):
    def create_cliente(self, email, username, password=None, **extra_fields):
        """
        Crea y guarda un usuario con el correo electrónico, nombre de usuario y contraseña proporcionados.
        """
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        if not username:
            raise ValueError('El nombre de usuario es obligatorio')
        email = self.normalize_email(email)
        cliente = self.model(email=email, username=username, **extra_fields)
        if password:
            cliente.password = make_password(password)
        cliente.save(using=self._db)
        return cliente

class Cliente(AbstractBaseUser):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    imagen = models.ImageField(upload_to='assets/uploads/clientes', blank=True)
    telefono = models.CharField(max_length=9)
    direccion = models.TextField()
    fecha_de_registro = models.DateTimeField(auto_now_add=True)

    objects = ClienteManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username + "'s Profile"

class Cupon(models.Model):
    codigo = models.CharField(max_length=8)
    descuento = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_expiracion = models.DateField(null=True, blank=True)
    cliente_que_lo_uso = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name='cupones_utilizados')

    def __str__(self):
        return self.codigo    
    
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