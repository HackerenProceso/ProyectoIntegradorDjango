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
    

@login_required
def groups(request):
    return render(request, 'pages/dashboards/groups.html')

@login_required
def users(request):
    return render(request, 'pages/dashboards/users.html')