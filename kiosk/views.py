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
        if 'bifocals' not in request.session:
            request.session['bifocals'] = request.POST.get("bifocals")
            print('Session var set!')
        if 'del_session' in request.POST:
            del request.session['bifocals']
            print('Session var unset!')
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