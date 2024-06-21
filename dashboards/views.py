from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.conf import settings
from django.urls import resolve
from Core.__init__ import KTLayout
from Core.libs.theme import KTTheme
from pprint import pprint
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from .forms import UserPasswordChangeForm
from django.contrib import admin
from django.utils import timezone
from .models import Cliente, Orden, Carrito, Producto, ProductoImagen
from datetime import datetime, date
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
"""
Landing Page Views
"""
# Create your views here.
def landing_page(request):
    return render(request, 'landing_page.html')

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to dashboards/urls.py file for more pages.
"""

class DashboardsView(LoginRequiredMixin, TemplateView):
    # Default template file
    template_name = 'pages/dashboards/index.html'
    
    # Redirige a la página de inicio de sesión si el usuario no está autenticado
    login_url = '/admin/signin/'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        # Initialize the global layout
        context = KTLayout.init(context)

        # Include vendors and javascript files for dashboard widgets
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])

        # Obtener la lista de modelos registrados en el panel de administración
        modelos = admin.site._registry.keys()

        # Separar los modelos en categorías
        auth_models = [model.__name__ for model in modelos if model._meta.app_label == 'auth']
        dashboard_models = [model.__name__ for model in modelos if model._meta.app_label == 'dashboards']

        # Agregar las listas de modelos al contexto
        context['auth_models'] = auth_models
        context['dashboard_models'] = dashboard_models
        
        # Calcular el total de todas las órdenes
        total_ordenes = Orden.objects.count()
        context['total_ordenes'] = total_ordenes

        # Calcular el total de carritos de hoy
        total_carritos_hoy = Carrito.objects.filter(creado_en__date=date.today()).count()
        context['total_carritos_hoy'] = total_carritos_hoy

        # Calcular el total de órdenes de hoy
        total_ordenes_hoy = Orden.objects.filter(creado_en__date=date.today()).count()
        context['total_ordenes_hoy'] = total_ordenes_hoy
       
        # Obtener el total de productos
        total_productos = Producto.objects.count()
        ultimos_productos = Producto.objects.order_by('-id')[:3]
        
        # Obtener los últimos 3 productos
        productos_adicionales  = max(total_productos - 3, 0)
        
        # Modificar la URL de la imagen en el contexto
        ultimos_productos_con_imagenes = []
        for producto in ultimos_productos:
            primera_imagen = producto.imagenes.first() if producto.imagenes.exists() else None
            ultimos_productos_con_imagenes.append({
                'producto': producto,
                'imagen_url': primera_imagen.imagen.url if primera_imagen else 'path/to/default/image.jpg'
            })
            
        # Calcular el total vendido de todas las órdenes
        total_vendido = Orden.objects.aggregate(Sum('total'))['total__sum'] or 0
        
         # Calcular el total vendido hoy
        hoy = timezone.now().date()
        start_of_day = datetime.combine(hoy, datetime.min.time())
        end_of_day = datetime.combine(hoy, datetime.max.time())

        total_vendido_hoy = Orden.objects.filter(creado_en__range=(start_of_day, end_of_day)).aggregate(Sum('total'))['total__sum'] or 0
        
        # Calcular el total de clientes registrados
        total_clientes = Cliente.objects.count()
        context['total_clientes'] = total_clientes
        
        # Calcular el total de clientes registrados hoy
        clientes_hoy = Cliente.objects.filter(fecha_de_registro__range=(start_of_day, end_of_day)).count()
        context['clientes_hoy'] = clientes_hoy
        
        context['total_vendido_hoy'] = total_vendido_hoy
        context['total_vendido'] = total_vendido
        context['total_productos'] = total_productos
        context['ultimos_productos'] = ultimos_productos_con_imagenes
        context['productos_adicionales'] = productos_adicionales
       
        
        return context
    
class UserProfileView(TemplateView):
    template_name = 'pages/dashboards/user_profile.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        # Initialize the global layout
        context = KTLayout.init(context)

        # Include vendors and javascript files for dashboard widgets
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        # Obtener la lista de modelos registrados en el panel de administración
        modelos = admin.site._registry.keys()

        # Separar los modelos en categorías
        auth_models = [model.__name__ for model in modelos if model._meta.app_label == 'auth']
        dashboard_models = [model.__name__ for model in modelos if model._meta.app_label == 'dashboards']

        # Agregar las listas de modelos al contexto
        context['auth_models'] = auth_models
        context['dashboard_models'] = dashboard_models
        return context
    

class UserChangePasswordView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/auth/new-password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        context['form'] = UserPasswordChangeForm(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        # Obtener el contexto común
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        
        form = UserPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Su contraseña ha sido actualizada con éxito.')
            return redirect('dashboards:change_password') 
        else:
            messages.error(request, 'Por favor, corrija los errores a continuación.')
            # Incluye 'layout' en el contexto para el renderizado de la plantilla
            context['form'] = form  # Agregar el formulario al contexto
            return render(request, self.template_name, context)

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.http import Http404

"""
Auth
"""
class CustomModelListView(ListView):
    template_name = 'pages/auth/viewModel.html'
    model = Group  # Establece el modelo a Group

    def get_queryset(self):
        model_name = self.kwargs['model_name']
        model = apps.get_model(app_label='auth', model_name=model_name)
        return model.objects.all() if model else model.objects.none()

    # En tu vista CustomModelListView
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.kwargs['model_name']
        model = apps.get_model(app_label='auth', model_name=model_name)

        if model:
            column_names = [field.name for field in model._meta.fields]
            model_objects = list(model.objects.values())
            processed_model_objects = [{column_name.lower().replace(" ", "_"): obj[column_name] for column_name in column_names} for obj in model_objects]

            context['column_names'] = column_names
            context['model_objects'] = processed_model_objects
            context['model_name'] = model_name

        modelos = admin.site._registry.keys()
        auth_models = [model.__name__ for model in modelos if model._meta.app_label == 'auth']
        dashboard_models = [model.__name__ for model in modelos if model._meta.app_label == 'dashboards']
        total_columns = len(context['column_names']) + 1 if 'column_names' in context else 1

        context.update({
            'auth_models': auth_models,
            'dashboard_models': dashboard_models,
            'total_columns': total_columns
        })

        # Inicializar el contexto común y agregar vendors de temas
        KTLayout.init(context)
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])

        return context
    
    def post(self, request, *args, **kwargs):
        model_name = self.kwargs['model_name']
        model = apps.get_model(app_label='auth', model_name=model_name)

        if model:
            if 'delete_all' in request.POST:
                model.objects.all().delete()
            elif 'delete_item_id' in request.POST:
                item_id = request.POST['delete_item_id']
                item = get_object_or_404(model, id=item_id)
                item.delete()

        return redirect(reverse('dashboards:auth_view', kwargs={'model_name': model_name}))
   
from django.shortcuts import render, redirect
from django.views.generic import View
from django.apps import apps
from django.forms import modelform_factory
from . import forms
from Core.__init__ import KTLayout
from Core.libs.theme import KTTheme

class AuthAddModelView(View):
    def get_context_data(self, **kwargs):
        context = {}
        model_name = kwargs['model_name']
        model = apps.get_model(app_label='auth', model_name=model_name)
        ModelForm = modelform_factory(model, exclude=[])

        context['model_name'] = model_name
        context['form'] = ModelForm()

        KTLayout.init(context)
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        
        modelos = admin.site._registry.keys()
        auth_models = [model.__name__ for model in modelos if model._meta.app_label == 'auth']
        dashboard_models = [model.__name__ for model in modelos if model._meta.app_label == 'dashboards']

        context.update({
            'auth_models': auth_models,
            'dashboard_models': dashboard_models,
            'user_model': User  # Agregar el modelo User al contexto
        })
        return context
    
    def post(self, request, model_name):
        model = apps.get_model(app_label='auth', model_name=model_name)
        
        if model:
            form_class = forms.UserForm if model_name == 'user' else None  # Manejar otros casos si es necesario
            if form_class:
                form = form_class(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    # Redirigir a una página de éxito (viewModel.html) pasando el nombre del modelo como contexto
                    context = self.get_context_data(model_name=model_name)  # Obtener el contexto actualizado
                    return render(request, 'pages/auth/addModel.html', {'model_name': model_name, **context})
                else:
                    context = self.get_context_data(model_name=model_name)
                    context['form'] = form
                    return render(request, 'pages/auth/addModel.html', context)
            else:
                # Manejar el caso donde no hay un formulario definido para el modelo
                return HttpResponse("Formulario no definido para este modelo.")
        else:
            # Manejar el caso donde el modelo no fue reconocido o no se pudo obtener
            return HttpResponse("Modelo no reconocido.")
         
from .forms import UserEditForm

class AuthEditModelView(View):
    template_name = 'pages/auth/editModel.html'

    def get(self, request, model_name, id):
        model = apps.get_model(app_label='auth', model_name=model_name)
        instance = get_object_or_404(model, id=id)
        form_instance = UserEditForm(instance=instance)
        context = {
            'form': form_instance,
            'model_name': model_name,
            'instance_id': id
        }

        # Inicializar el contexto común y agregar vendors de temas
        KTLayout.init(context)
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        modelos = admin.site._registry.keys()
        auth_models = [model.__name__ for model in modelos if model._meta.app_label == 'auth']
        dashboard_models = [model.__name__ for model in modelos if model._meta.app_label == 'dashboards']

        context.update({
            'auth_models': auth_models,
            'dashboard_models': dashboard_models
        })

        return render(request, self.template_name, context)
    
    def post(self, request, model_name, id):
        model = apps.get_model(app_label='auth', model_name=model_name)
        instance = get_object_or_404(model, id=id)
        form_class = modelform_factory(model, exclude=[])
        form_instance = form_class(request.POST, instance=instance)

        if form_instance.is_valid():
            form_instance.save()
            return redirect(reverse('dashboards:auth_view', kwargs={'model_name': model_name}))

        context = {
            'form': form_instance,
            'model_name': model_name,
            'instance_id': id
        }

        # Inicializar el contexto común y agregar vendors de temas
        KTLayout.init(context)
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        modelos = admin.site._registry.keys()
        
        auth_models = [model.__name__ for model in modelos if model._meta.app_label == 'auth']
        dashboard_models = [model.__name__ for model in modelos if model._meta.app_label == 'dashboards']

        context.update({
            'auth_models': auth_models,
            'dashboard_models': dashboard_models
        })

        return render(request, self.template_name, context)
   
 
"""
Dashboards
"""
from django.apps import apps
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django.contrib import admin

class CustomModelsView(ListView):
    template_name = 'pages/dashboards/viewModel.html'

    def get_queryset(self):
        model_name = self.kwargs['model_name']
        model = apps.get_model(app_label='dashboards', model_name=model_name)
        return model.objects.all() if model else model.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.kwargs['model_name']
        model = apps.get_model(app_label='dashboards', model_name=model_name)
        context['image_base_url'] = settings.MEDIA_URL  
        
        if model:
            column_names = [field.name for field in model._meta.fields]
            model_objects = list(model.objects.values())
            processed_model_objects = [{column_name.lower().replace(" ", "_"): obj[column_name] for column_name in column_names if column_name in obj} for obj in model_objects]


            context['column_names'] = column_names
            context['model_objects'] = processed_model_objects
            context['model_name'] = model_name

        modelos = admin.site._registry.keys()
        auth_models = [model.__name__ for model in modelos if model._meta.app_label == 'auth']
        dashboard_models = [model.__name__ for model in modelos if model._meta.app_label == 'dashboards']
        total_columns = len(context['column_names']) + 1 if 'column_names' in context else 1

        context.update({
            'auth_models': auth_models,
            'dashboard_models': dashboard_models,
            'total_columns': total_columns
        })

        # Inicializar el contexto común y agregar vendors de temas
        KTLayout.init(context)
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])

        return context
    
    def post(self, request, *args, **kwargs):
        model_name = self.kwargs['model_name']
        model = apps.get_model(app_label='dashboards', model_name=model_name)

        if model:
            if 'delete_all' in request.POST:
                model.objects.all().delete()
            elif 'delete_item_id' in request.POST:
                item_id = request.POST['delete_item_id']
                item = get_object_or_404(model, id=item_id)
                item.delete()

        return redirect(reverse('dashboards:model_view', kwargs={'model_name': model_name}))

    

from django.shortcuts import render, redirect
from django.views.generic import View
from django.apps import apps
from django.forms import modelform_factory
from . import forms
from Core.__init__ import KTLayout
from Core.libs.theme import KTTheme

class AddModelView(View):
    def get_context_data(self, **kwargs):
        context = {}

        model_name = kwargs['model_name']
        model = apps.get_model(app_label='dashboards', model_name=model_name)
        ModelForm = modelform_factory(model, exclude=[])

        context['model_name'] = model_name
        context['form'] = ModelForm()

        KTLayout.init(context)
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        
        modelos = admin.site._registry.keys()
        auth_models = [model.__name__ for model in modelos if model._meta.app_label == 'auth']
        dashboard_models = [model.__name__ for model in modelos if model._meta.app_label == 'dashboards']

        context.update({
            'auth_models': auth_models,
            'dashboard_models': dashboard_models
        })
        return context
    
    def get(self, request, model_name):
        try:
            form_class = getattr(forms, f'{model_name}')
        except AttributeError:
            form_class = forms.producto

        context = self.get_context_data(model_name=model_name)
        context['form'] = form_class()

        return render(request, 'pages/dashboards/addModel.html', context)
    
    def post(self, request, model_name):
        try:
            form_class = getattr(forms, f'{model_name}')
        except AttributeError:
            form_class = forms.producto if model_name == 'producto' else forms.cliente

        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            if model_name == 'productoimagen':
                # Verificar si el formulario tiene el campo 'producto'
                producto = form.cleaned_data['producto']
                imagenes = request.FILES.getlist('imagenes')

                for imagen in imagenes:
                    ProductoImagen.objects.create(producto=producto, imagen=imagen)
            form.save()
             # Redirigir a la URL del DashboardsView
            return redirect('dashboards:index')
        else:
            context = self.get_context_data(model_name=model_name)
            context['form'] = form
            return render(request, 'pages/dashboards/addModel.html', context)
        
        
from django.views.generic import View
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.apps import apps
from django.forms import modelform_factory
from Core.__init__ import KTLayout
from Core.libs.theme import KTTheme

class EditModelView(View):
    template_name = 'pages/dashboards/editModel.html'

    def get(self, request, model_name, id):
        model = apps.get_model(app_label='dashboards', model_name=model_name)
        instance = get_object_or_404(model, id=id)
        form_class = modelform_factory(model, exclude=[])
        form_instance = form_class(instance=instance)
        context = {
            'form': form_instance,
            'model_name': model_name,
            'instance_id': id
        }

        # Inicializar el contexto común y agregar vendors de temas
        KTLayout.init(context)
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        modelos = admin.site._registry.keys()
        auth_models = [model.__name__ for model in modelos if model._meta.app_label == 'auth']
        dashboard_models = [model.__name__ for model in modelos if model._meta.app_label == 'dashboards']

        context.update({
            'auth_models': auth_models,
            'dashboard_models': dashboard_models
        })

        return render(request, self.template_name, context)
    
    def post(self, request, model_name, id):
        model = apps.get_model(app_label='dashboards', model_name=model_name)
        instance = get_object_or_404(model, id=id)
        form_class = modelform_factory(model, exclude=[])
        form_instance = form_class(request.POST, instance=instance)

        if form_instance.is_valid():
            form_instance.save()
            return redirect(reverse('dashboards:model_view', kwargs={'model_name': model_name}))

        context = {
            'form': form_instance,
            'model_name': model_name,
            'instance_id': id
        }

        # Inicializar el contexto común y agregar vendors de temas
        KTLayout.init(context)
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        modelos = admin.site._registry.keys()
        
        auth_models = [model.__name__ for model in modelos if model._meta.app_label == 'auth']
        dashboard_models = [model.__name__ for model in modelos if model._meta.app_label == 'dashboards']

        context.update({
            'auth_models': auth_models,
            'dashboard_models': dashboard_models
        })

        return render(request, self.template_name, context)

#Ordenes
from django.shortcuts import render
from django.views import View
from .models import Orden

class ReceiptsListView(View):
    template_name = 'pages/recibos/recibos_list.html'
    
    def get(self, request):
        recibos = Orden.objects.all()
        context = {
            'recibos': recibos
        }
        return render(request, self.template_name, context)

from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Orden
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.template import Context

class ReciboDetailView(View):
    template_name = 'pages/recibos/recibo_detail.html'

    def get(self, request, recibo_id):
        recibo = get_object_or_404(Orden, id=recibo_id)
        context = {
            'recibo': recibo
        }
        return render(request, self.template_name, context)

@login_required
def enviar_correo(request):
    if request.method == 'POST':
        emails = request.POST.get('emails')  # Cambiar 'email' a 'emails'
        recibo_id = request.POST.get('recibo_id')

        # Obtener el recibo específico usando el ID
        recibo = get_object_or_404(Orden, pk=recibo_id)

        # Renderizar el contenido del recibo con los datos específicos
        html_content = render_to_string('pages/recibos/detalle_recibo_content.html', {'recibo': recibo})

        # Crear el mensaje de correo
        email_subject = 'Detalle del Recibo'
        email_body = 'Se adjunta el detalle del recibo.'
        from_email = settings.DEFAULT_FROM_EMAIL
        
        # Dividir la cadena de correos por comas y limpiar espacios en blanco
        email_list = [email.strip() for email in emails.split(',')]
        
        # Enviar el correo a cada destinatario en la lista
        for email in email_list:
            email_message = EmailMultiAlternatives(
                subject=email_subject,
                body=email_body,
                from_email=from_email,
                to=[email]
            )

            # Agregar el contenido HTML al cuerpo del correo electrónico
            email_message.attach_alternative(html_content, "text/html")

            try:
                email_message.send()
            except Exception as e:
                # Manejar cualquier error al enviar el correo
                messages.error(request, f"Error al enviar el correo a {email}: {str(e)}")
                return redirect('dashboards:recibos_list')

        # Mostrar mensaje de éxito
        messages.success(request, "Correo enviado correctamente.")
        return redirect('dashboards:recibos_list')
    
    return redirect('dashboards:recibos_list')