from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined']
        widgets = {
            'id': forms.HiddenInput(),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'last_login': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Enter last login', 'type': 'date'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'date_joined': forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Enter date joined'}),
        }

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Contraseña Anterior",
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-transparent', 'placeholder': 'Contraseña Anterior'})
    )
    new_password1 = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-transparent', 'placeholder': 'Nueva Contraseña'})
    )
    new_password2 = forms.CharField(
        label="Repite Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-transparent', 'placeholder': 'Repite Nueva Contraseña'})
    )

# forms.py
from django import forms
from .models import Perfil, Producto, ProductoImagen, Marca, Categoria, Cupon, Cliente, Orden, DetalleOrden, Carrito, DetalleCarrito, Review
from django import forms
from multiupload.fields import MultiFileField
from .models import ProductoImagen
from django.contrib.auth.hashers import make_password

class perfil(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'
        widgets = {
            'imagen': forms.FileInput(attrs={'class': 'form-control-file', 'id': 'imagen-input'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'user': forms.Select(attrs={'class': 'form-control'}),
        }

class producto(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(producto, self).__init__(*args, **kwargs)
        self.fields['marca'].widget = forms.Select(choices=self.get_marca_choices(), attrs={'class': 'form-control'})
        self.fields['categoria'].widget = forms.Select(choices=self.get_categoria_choices(), attrs={'class': 'form-control'})

    def get_marca_choices(self):
        return [(marca.id, marca.nombre) for marca in Marca.objects.all()]

    def get_categoria_choices(self):
        return [(categoria.id, categoria.nombre) for categoria in Categoria.objects.all()]

    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'lote': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class productoimagen(forms.ModelForm):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), empty_label=None, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    imagenes = MultiFileField(max_num=5, max_file_size=1024*1024, required=False)

    class Meta: 
        model = ProductoImagen
        fields = ['producto', 'imagenes']
 
class marca(forms.ModelForm):
    class Meta:
        model = Marca
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la marca'}),
        }

class categoria(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción de la categoría', 'rows': 3}),
        }

class cupon(forms.ModelForm):
    class Meta:
        model = Cupon
        fields = '__all__'
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código del cupón'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de cupón'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Descuento'}),
            'fecha_expiracion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'usado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class cliente(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control-file', 'id': 'imagen-input'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Dirección', 'rows': 3}),
            'fecha_de_registro': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'last_login': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def save(self, commit=True):
        # Guardar la contraseña de forma segura usando make_password
        self.instance.password = make_password(self.cleaned_data['password'])
        return super().save(commit=commit)

class orden(forms.ModelForm):
    class Meta:
        model = Orden
        fields = '__all__'
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class detalleorden(forms.ModelForm):
    class Meta:
        model = DetalleOrden
        fields = '__all__'
        widgets = {
            'orden': forms.Select(attrs={'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': True}),
        }


class carrito(forms.ModelForm):
    class Meta:
        model = Carrito
        fields = '__all__'
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'fecha_creacion': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'orden_asociada': forms.Select(attrs={'class': 'form-control'}),
        }

class detallecarrito(forms.ModelForm):
    class Meta:
        model = DetalleCarrito
        fields = '__all__'
        widgets = {
            'carrito': forms.Select(attrs={'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
        }


class review(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['producto', 'comentario', 'estrellas']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'estrellas': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

    def __init__(self, *args, **kwargs):
        super(review, self).__init__(*args, **kwargs)
        self.fields['producto'].empty_label = "Seleccione un producto"