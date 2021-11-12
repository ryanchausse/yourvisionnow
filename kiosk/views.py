from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import RequestContext


class KioskPage(TemplateView):
    """
    First page at root - kiosk view
    """
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        if 'start_over' in request.POST and request.POST['start_over'] == 'true':
            # Delete session
            request.session.flush()
        # Single Vision Lens - later change to be database-driven
        if 'no_single_vision' in request.POST:
            del request.session['lens_single_vision']
        if request.POST.get('lens_single_vision') and 'lens_single_vision' not in request.session:
            request.session['lens_single_vision'] = request.POST.get('lens_single_vision')
        # Bifocal - later change to be database-driven
        if 'no_bifocal' in request.POST:
            del request.session['lens_bifocal']
        if request.POST.get('lens_bifocal') and 'lens_bifocal' not in request.session:
            request.session['lens_bifocal'] = request.POST.get('lens_bifocal')
        # Trifocal - later change to be database-driven
        if 'no_trifocal' in request.POST:
            del request.session['lens_trifocal']
        if request.POST.get('lens_trifocal') and 'lens_bifocal' not in request.session:
            request.session['lens_trifocal'] = request.POST.get('lens_trifocal')
        # Progressive - later change to be database-driven
        if 'no_progressive' in request.POST:
            del request.session['lens_progressive']
        if request.POST.get('lens_progressive') and 'lens_progressive' not in request.session:
            request.session['lens_progressive'] = request.POST.get('lens_progressive')
        return redirect('/')


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