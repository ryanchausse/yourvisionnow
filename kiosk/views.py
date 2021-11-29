from django.shortcuts import render
from django.contrib.auth.models import User, Group
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
        if self.request.user.groups.filter(name='Admins').exists():
            context['user_is_in_admins'] = True
        else:
            context['user_is_in_admins'] = False
        context['lens_types'] = LensType.objects.all().order_by('-default_price')
        context['lens_materials'] = LensMaterial.objects.all().order_by('-default_price')
        context['lens_add_ons'] = LensAddOns.objects.all().order_by('-default_price')
        context['lens_packages'] = LensPackage.objects.all().order_by('-retail_price')
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        lens_type, lens_package, lens_material, lens_add_ons = dict(), dict(), dict(), dict()
        choices = [lens_type, lens_package, lens_material, lens_add_ons]

        for lens_type in context['lens_types']:
            if f'no_{lens_type.name}' in request.POST:
                if request.session[lens_type.name]:
                    request.session['lens_type_selected'] = False
                    del request.session[lens_type.name]
            if request.POST.get(lens_type.name) and request.POST.get(lens_type.name) not in request.session:
                request.session['lens_type_selected'] = True
                request.session[lens_type.name] = True
        for lens_material in context['lens_materials']:
            if f'no_{lens_material.name}' in request.POST:
                if request.session[lens_material.name]:
                    request.session['lens_material_selected'] = False
                    del request.session[lens_material.name]
            if request.POST.get(lens_material.name) and request.POST.get(lens_material.name) not in request.session:
                request.session['lens_material_selected'] = True
                request.session[lens_material.name] = True
            if 'no_lens_materials' in request.POST and request.POST.get('no_lens_materials') == 'true':
                if lens_material.name in request.session:
                    del request.session[lens_material.name]
                request.session['lens_material_selected'] = True
                request.session['no_lens_materials'] = True
            if 'reset_lens_materials' in request.POST and request.POST.get('reset_lens_materials') == 'true':
                request.session['lens_material_selected'] = False
                request.session['no_lens_materials'] = False
        for lens_add_on in context['lens_add_ons']:
            if f'no_{lens_add_on.name}' in request.POST:
                if request.session[lens_add_on.name]:
                    request.session['lens_add_on_selected'] = False
                    del request.session[lens_add_on.name]
            if request.POST.get(lens_add_on.name) and request.POST.get(lens_add_on.name) not in request.session:
                request.session['lens_add_on_selected'] = True
                request.session[lens_add_on.name] = True
            if 'no_lens_add_ons' in request.POST and request.POST.get('no_lens_add_ons') == 'true':
                if lens_add_on.name in request.session:
                    del request.session[lens_add_on.name]
                request.session['lens_add_on_selected'] = True
                request.session['no_lens_add_ons'] = True
            if 'reset_lens_add_ons' in request.POST and request.POST.get('reset_lens_add_ons') == 'true':
                request.session['lens_add_on_selected'] = False
                request.session['no_lens_add_ons'] = False
        for lens_package in context['lens_packages']:
            if f'no_{lens_package.name}' in request.POST:
                if request.session[lens_package.name]:
                    request.session['lens_package_selected'] = False
                    del request.session[lens_package.name]
            if request.POST.get(lens_package.name) and request.POST.get(lens_package.name) not in request.session:
                request.session['lens_package_selected'] = True
                request.session[lens_package.name] = True
            if 'no_lens_packages' in request.POST and request.POST.get('no_lens_packages') == 'true':
                if lens_package.name in request.session:
                    del request.session[lens_package.name]
                request.session['lens_package_selected'] = True
                request.session['no_lens_packages'] = True
            if 'reset_lens_packages' in request.POST and request.POST.get('reset_lens_packages') == 'true':
                request.session['lens_package_selected'] = False
                request.session['no_lens_packages'] = False

        if 'first_name' in request.POST:
            first_name = request.POST.get('first_name')
            request.session['first_name'] = first_name
            context['first_name'] = first_name
        elif 'first_name' in request.session:
            context['first_name'] = request.session['first_name']

        if request.user.groups.filter(name='Admins').exists():
            context['user_is_in_admins'] = True
        else:
            context['user_is_in_admins'] = False

        return render(request, 'index.html', context)


class SubmitOrder(TemplateView):
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'done' in request.POST and request.POST['done'] == 'true':
            # First, get or create Customer if none exists
            first_name = ''
            last_name = ''
            email = ''
            if request.user.is_authenticated:
                if request.user.first_name:
                    first_name = request.user.first_name
                if request.user.last_name:
                    last_name = request.user.last_name
                if request.user.email:
                    email = request.user.email
            else:
                if 'first_name' in request.session:
                    first_name = request.session['first_name']
                if 'last_name' in request.session:
                    last_name = request.session['last_name']
                if 'email' in request.session:
                    email = request.session['email']
            customer, created = Customer.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            if created:
                print(f'New customer created: {customer.first_name} {customer.last_name}')

            # Next, make notes for Order
            order_notes = ''
            for key, value in request.session.items():
                # First statement to see whether variable is framework-based;
                # second statement to remove vars that have been set and used only internally
                if key[0] != '_' and "_" not in key:
                    order_notes += key + ', '
            if order_notes and order_notes[-2::] == ', ':
                order_notes = order_notes[:-2]
            order = Order.objects.create(
                name=customer.first_name + '\'s order',
                customer=customer,
                notes=order_notes
            )
            order.save()
            send_mail(
                'Customer order',
                f'New order:\n\n{order_notes}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            request.session.flush()
        return redirect('/index.html')


class WelcomePage(TemplateView):
    """
    First / Login page at root
    """
    template_name = 'index.html'


class ManagerPage(TemplateView):
    """
    Front desk / manager page to list orders
    """
    template_name = 'manager.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Admins').exists():
            context = self.get_context_data(**kwargs)
            context['orders'] = Order.objects.all().order_by('-created_at')
            return render(request,
                          template_name=self.template_name,
                          context=context)
        else:
            return redirect('/index.html')


class ManagerLensPackagePage(TemplateView):
    """
    Manager's CRUD for Lens Packages
    """
    template_name = 'manager_lens_packages.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Admins').exists():
            context = self.get_context_data(**kwargs)
            context['lens_packages'] = LensPackage.objects.all().order_by('-created_at')
            return render(request,
                          template_name=self.template_name,
                          context=context)
        else:
            return redirect('/index.html')


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