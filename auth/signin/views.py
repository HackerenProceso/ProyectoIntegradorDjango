from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings
from Core.__init__ import KTLayout
from Core.libs.theme import KTTheme

class AuthSigninView(TemplateView):
    template_name = 'pages/auth/signin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addJavascriptFile('js/custom/authentication/sign-in/general.js')
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })
        return context

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirigir al panel de control después del inicio de sesión exitoso
            return redirect(reverse('dashboards:index'))
        else:
            context = self.get_context_data(**kwargs)
            context['error'] = 'Invalid username or password'
            return render(request, self.template_name, context)