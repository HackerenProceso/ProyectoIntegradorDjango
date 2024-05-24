from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('auth:signin')  # Redirige a la página de inicio de sesión
