from django.shortcuts import render
from django.views.generic import TemplateView
from pprint import pprint
from Core.__init__ import KTLayout
from Core.libs.theme import KTTheme
from django.contrib.admin import site

class SystemView(TemplateView):
    template_name = 'pages/system/not-found.html'
    status = ''

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in Core/__init__.py file
        context = KTLayout.init(context)

        # Define the layout for this module
        # _templates/layout/system.html
        context.update({
            'layout': KTTheme.setLayout('system.html', context),
            'status': self.status,
        })

        return context
