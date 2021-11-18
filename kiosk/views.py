from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import RequestContext
import logging
from django.conf import settings
from .models import Customer
from .models import LensType
from .models import LensMaterial
from .models import LensAddOns
from .models import LensPackage
from .models import LensPackageItem
from .models import Order


class KioskPage(TemplateView):
    """
    First page at root - kiosk view
    """
    template_name = 'index.html'
    logger = logging.getLogger(__name__)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lens_types'] = LensType.objects.all()
        context['lens_materials'] = LensMaterial.objects.all()
        context['lens_add_ons'] = LensAddOns.objects.all()
        context['lens_packages'] = LensPackage.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'start_over' in request.POST and request.POST['start_over'] == 'true':
            # Delete session
            request.session.flush()
        if 'done' in request.POST and request.POST['done'] == 'true':
            session_info = ''
            for key, value in request.session.items():
                session_info += f'{ key }: { value }\n'
            print(session_info)
            print(settings.EMAIL_HOST_USER)
            send_mail(
                'Customer order',
                f'New order:\n\n{ session_info }',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            request.session.flush()
        for lens_type in context['lens_types']:
            if f'no_{lens_type.name}' in request.POST:
                if request.session[lens_type.name]:
                    del request.session[lens_type.name]
            if request.POST.get(lens_type.name) and request.POST.get(lens_type.name) not in request.session:
                request.session[lens_type.name] = True
        for lens_material in context['lens_materials']:
            if f'no_{lens_material.name}' in request.POST:
                if request.session[lens_material.name]:
                    del request.session[lens_material.name]
            if request.POST.get(lens_material.name) and request.POST.get(lens_material.name) not in request.session:
                request.session[lens_material.name] = True
        for lens_add_on in context['lens_add_ons']:
            if f'no_{lens_add_on.name}' in request.POST:
                if request.session[lens_add_on.name]:
                    del request.session[lens_add_on.name]
            if request.POST.get(lens_add_on.name) and request.POST.get(lens_add_on.name) not in request.session:
                request.session[lens_add_on.name] = True
        for lens_package in context['lens_packages']:
            if f'no_{lens_package.name}' in request.POST:
                if request.session[lens_package.name]:
                    del request.session[lens_package.name]
            if request.POST.get(lens_package.name) and request.POST.get(lens_package.name) not in request.session:
                request.session[lens_package.name] = True
        if 'first_name' in request.POST:
            first_name = request.POST.get('first_name')
            request.session['first_name'] = first_name
            context['first_name'] = first_name
        elif 'first_name' in request.session:
            context['first_name'] = request.session['first_name']

        return render(request, 'index.html', context)


class WelcomePage(TemplateView):
    """
    First / Login page at root
    """
    template_name = 'index.html'


def handler404(request, exception, template_name="404.html"):
    """
    Custom 404 page
    """
    response = render(template_name)
    response.status_code = 404
    return response


def handler500(request, exception, template_name="500.html"):
    """
    Custom 500 page
    """
    response = render(template_name)
    response.status_code = 500
    return response


def index(request):
    """
    Old/beginning index view
    """
    return HttpResponse('Go to <a href="./kiosk">Kiosk</a> or \
                        Log In using <a href="./accounts/google/login">Google</a> \
                        <br /> or Log Out <a href="./accounts/logout">Here</a>.')