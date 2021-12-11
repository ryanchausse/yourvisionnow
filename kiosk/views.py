from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import RequestContext
from django.core import serializers
from django.forms.models import model_to_dict
import logging
from django.conf import settings
from .models import Customer
from .models import LensType
from .models import LensMaterial
from .models import LensAddOns
from .models import LensPackage
from .models import LensPackageItem
from .models import Order
from .models import LensDesign
from .models import LensDesignItem


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
        context['lens_types'] = LensType.objects.all().order_by('-order_position')
        context['lens_materials'] = LensMaterial.objects.all().order_by('-order_position')
        context['lens_add_ons'] = LensAddOns.objects.all().order_by('-order_position')
        # context['lens_packages'] = LensPackage.objects.all().order_by('-retail_price')
        context['lens_designs'] = LensDesign.objects.all().order_by('-order_position')
        return context

    def post(self, request, *args, **kwargs):
        """
            1. Present user with lens type choice
            2. Present user with lens design choice
            3. Lens material choice
            4. Lens add-on choice
        """
        context = self.get_context_data(**kwargs)

        for lens_type in context['lens_types']:
            if f'no_{lens_type.name}' in request.POST:
                self.hierarchical_reset('lens_type', request, context)
            if request.POST.get(lens_type.name) and request.POST.get(lens_type.name) not in request.session:
                self.set_item('lens_type', lens_type.name, request, context)
            if lens_type.name in request.session:
                lens_design_items = LensDesignItem.objects.filter(
                    lens_type=LensType.objects.get(name=lens_type.name)
                ).distinct('lens_design')
                context['lens_design_choices'] = lens_design_items
        for lens_design in context['lens_designs']:
            if request.POST.get(lens_design.name) and request.POST.get(lens_design.name) not in request.session:
                self.set_item('lens_design', lens_design.name, request, context)
            if 'no_lens_designs' in request.POST and request.POST.get('no_lens_designs') == 'true':
                self.none_button_selected('lens_design', request, context)
            if 'reset_lens_designs' in request.POST and request.POST.get('reset_lens_designs') == 'true':
                self.reset_items('lens_design', request, context)
            if f'no_{lens_design.name}' in request.POST:
                self.hierarchical_reset('lens_design', request, context)
            # The latter fields will depend on the selected Lens Design and derive from
            # the LensDesignItem model
            if lens_design.name in request.session:
                for lens_type in context['lens_types']:
                    if lens_type.name in request.session:
                        lens_material_items = LensDesignItem.objects.filter(
                            lens_design=LensDesign.objects.get(name=lens_design.name),
                            lens_type=LensType.objects.get(name=lens_type.name)
                        ).distinct('lens_material')
                        context['lens_material_choices'] = lens_material_items
        for lens_material in context['lens_materials']:
            if request.POST.get(lens_material.name) and request.POST.get(lens_material.name) not in request.session:
                self.set_item('lens_material', lens_material.name, request, context)
            if lens_material.name in request.session:
                for lens_type in context['lens_types']:
                    if lens_type.name in request.session:
                        lens_type_name = lens_type.name
                for lens_design in context['lens_designs']:
                    if lens_design.name in request.session:
                        lens_design_name = lens_design.name
                lens_add_on_items = LensDesignItem.objects.filter(
                    lens_type=LensType.objects.get(name=lens_type_name),
                    lens_design=LensDesign.objects.get(name=lens_design_name),
                    lens_material=LensMaterial.objects.get(name=lens_material.name)
                ).distinct('lens_add_on')
                context['lens_add_on_choices'] = lens_add_on_items
            if 'no_lens_materials' in request.POST and request.POST.get('no_lens_materials') == 'true':
                self.none_button_selected('lens_material', request, context)
            if 'reset_lens_materials' in request.POST and request.POST.get('reset_lens_materials') == 'true':
                self.reset_items('lens_material', request, context)
            if f'no_{lens_material.name}' in request.POST:
                self.hierarchical_reset('lens_material', request, context)
        for lens_add_on in context['lens_add_ons']:
            if request.POST.get(lens_add_on.name) and request.POST.get(lens_add_on.name) not in request.session:
                self.set_item('lens_add_on', lens_add_on.name, request, context)
            if 'no_lens_add_ons' in request.POST and request.POST.get('no_lens_add_ons') == 'true':
                self.none_button_selected('lens_add_on', request, context)
            if 'reset_lens_add_ons' in request.POST and request.POST.get('reset_lens_add_ons') == 'true':
                self.reset_items('lens_add_on', request, context)
            if f'no_{lens_add_on.name}' in request.POST:
                self.hierarchical_reset('lens_add_on', request, context)

        self.set_first_name(request, context)
        self.set_admin(request, context)
        return render(request, 'index.html', context)

    @staticmethod
    def set_item(item, item_name, request, context):
        print(f'set item: { item_name }')
        if item == 'lens_type':
            request.session['lens_type_selected'] = True
            request.session[item_name] = True
        if item == 'lens_design':
            request.session['lens_design_selected'] = True
            request.session[item_name] = True
        if item == 'lens_material':
            request.session['lens_material_selected'] = True
            request.session[item_name] = True
        if item == 'lens_add_on':
            request.session['lens_add_on_selected'] = True
            request.session[item_name] = True

    @staticmethod
    def no_on_item(item, item_name, request, context):
        print(f'no on item: { item_name }')
        if item == 'lens_type':
            if item_name in request.session:
                request.session['lens_type_selected'] = False
                del request.session[item_name]
        if item == 'lens_design':
            if item_name in request.session:
                request.session['lens_design_selected'] = False
                del request.session[item_name]
        if item == 'lens_material':
            if item_name in request.session:
                request.session['lens_material_selected'] = False
                del request.session[item_name]
        if item == 'lens_add_on':
            if item_name in request.session:
                request.session['lens_add_on_selected'] = False
                del request.session[item_name]

    @staticmethod
    def none_button_selected(item_name, request, context):
        # when the user hits e.g. 'No lens Add-Ons'
        if item_name == 'lens_design':
            if item_name in request.session:
                del request.session[item_name]
            request.session['lens_design_selected'] = True
            request.session['no_lens_designs'] = True
        if item_name == 'lens_material':
            if item_name in request.session:
                del request.session[item_name]
            request.session['lens_naterial_selected'] = True
            request.session['no_lens_materials'] = True
        if item_name == 'lens_add_on':
            if item_name in request.session:
                del request.session[item_name]
            request.session['lens_add_on_selected'] = True
            request.session['no_lens_add_ons'] = True

    @staticmethod
    def reset_items(item_name, request, context):
        if item_name == 'lens_types':
            request.session['lens_type_selected'] = False
            request.session['no_lens_types'] = False
        if item_name == 'lens_designs':
            request.session['lens_design_selected'] = False
            request.session['no_lens_designs'] = False
        if item_name == 'lens_materials':
            request.session['lens_material_selected'] = False
            request.session['no_lens_materials'] = False
        if item_name == 'lens_add_ons':
            request.session['lens_add_on_selected'] = False
            request.session['no_add_ons'] = False

    def hierarchical_reset(self, item, request, context):
        if item == 'lens_type':
            for lens_type in context['lens_types']:
                self.no_on_item('lens_type', lens_type.name, request, context)
            request.session['lens_type_selected'] = False
            request.session['no_lens_types'] = False
            for lens_design in context['lens_designs']:
                self.no_on_item('lens_design', lens_design.name, request, context)
            request.session['lens_design_selected'] = False
            request.session['no_lens_designs'] = False
            for lens_material in context['lens_materials']:
                self.no_on_item('lens_material', lens_material.name, request, context)
            request.session['lens_material_selected'] = False
            request.session['no_lens_materials'] = False
            for lens_add_on in context['lens_add_ons']:
                self.no_on_item('lens_add_on', lens_add_on.name, request, context)
            request.session['lens_add_on_selected'] = False
            request.session['no_add_ons'] = False
        if item == 'lens_design':
            for lens_design in context['lens_designs']:
                self.no_on_item('lens_design', lens_design.name, request, context)
            request.session['lens_design_selected'] = False
            request.session['no_lens_designs'] = False
            for lens_material in context['lens_materials']:
                self.no_on_item('lens_material', lens_material.name, request, context)
            request.session['lens_material_selected'] = False
            request.session['no_lens_materials'] = False
            for lens_add_on in context['lens_add_ons']:
                self.no_on_item('lens_add_on', lens_add_on.name, request, context)
            request.session['lens_add_on_selected'] = False
            request.session['no_add_ons'] = False
        if item == 'lens_material':
            for lens_material in context['lens_materials']:
                self.no_on_item('lens_material', lens_material.name, request, context)
            request.session['lens_material_selected'] = False
            request.session['no_lens_materials'] = False
            for lens_add_on in context['lens_add_ons']:
                self.no_on_item('lens_add_on', lens_add_on.name, request, context)
            request.session['lens_add_on_selected'] = False
            request.session['no_add_ons'] = False
        if item == 'lens_add_on':
            for lens_add_on in context['lens_add_ons']:
                self.no_on_item('lens_add_on', lens_add_on.name, request, context)
            request.session['lens_add_on_selected'] = False
            request.session['no_add_ons'] = False

    @staticmethod
    def set_first_name(request, context):
        if 'first_name' in request.POST:
            first_name = request.POST.get('first_name')
            request.session['first_name'] = first_name
            context['first_name'] = first_name
        elif 'first_name' in request.session:
            context['first_name'] = request.session['first_name']

    @staticmethod
    def set_admin(request, context):
        if request.user.groups.filter(name='Admins').exists():
            context['user_is_in_admins'] = True
        else:
            context['user_is_in_admins'] = False


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
            if customer.first_name:
                first_name = customer.first_name
            if customer.last_name:
                last_name = customer.last_name
            if customer.email:
                email = customer.email
            send_mail(
                'Customer order',
                f'New order:\n\n'
                f'{order_notes}\n\n'
                f'Customer info (if applicable):\n\n'
                f'Name: {first_name} {last_name}\n\n'
                f'Email: {email}',
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