from django.urls import path, include
from django.conf import settings
from dashboards.views import DashboardsView
from dashboards import views as d_views
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

app_name = 'dashboards'

urlpatterns = [
    path('', DashboardsView.as_view(template_name = 'pages/dashboards/index.html'), name='index'),
    path('error', DashboardsView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
    
    #User
    path('profile/', d_views.UserProfileView.as_view(), name='user_profile'),
    path('change-password/', d_views.UserChangePasswordView.as_view(), name='change_password'),
    
    #Admin models Auth
    path('auth/<str:model_name>/', d_views.CustomModelListView.as_view(), name='auth_view'),
    path('auth/<str:model_name>/add/', d_views.AuthAddModelView.as_view(), name='auth_add_model'),
    path('auth/<str:model_name>/edit/<int:id>/', d_views.AuthEditModelView.as_view(), name='auth_edit_model'),
    
    #Admin models Dashboards
    path('dashboard/<str:model_name>/', d_views.CustomModelsView.as_view(), name='model_view'),
    path('dashboard/<str:model_name>/add/', d_views.AddModelView.as_view(), name='add_model'),
    path('dashboard/<str:model_name>/edit/<int:id>/', d_views.EditModelView.as_view(), name='edit_model'),
    
    # Recibos
    path('recibos/', views.ReceiptsListView.as_view(), name='recibos_list'),
    path('recibos/<int:recibo_id>/', views.ReciboDetailView.as_view(), name='recibo_view'),
    path('recibos/enviar_correo/', views.enviar_correo, name='enviar_correo'),
]