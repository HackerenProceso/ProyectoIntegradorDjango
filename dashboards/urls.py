from django.urls import path, include
from django.conf import settings
from dashboards.views import DashboardsView
from dashboards import views as d_views
from . import views

app_name = 'dashboards'

urlpatterns = [
    path('', DashboardsView.as_view(template_name = 'pages/dashboards/index.html'), name='index'),
    path('error', DashboardsView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
    
    #User
    path('profile/', d_views.UserProfileView.as_view(), name='user_profile'),
    
    path('groups/', views.groups, name='groups'),
    path('users/', views.users, name='users'),
    path('admin/', include('django.contrib.admin.urls')),  # Incluye las vistas de administración de Django
]

#<a href="{% url 'dashboards:index' %}">
