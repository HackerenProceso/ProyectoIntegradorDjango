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
        form_class = getattr(forms, f'{model_name}')
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirigir a una página de éxito (viewModel.html) pasando el nombre del modelo como contexto
            context = self.get_context_data(model_name=model_name)  # Obtener el contexto actualizado
            return render(request, 'pages/dashboards/addModel.html', {'model_name': model_name, **context})
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
