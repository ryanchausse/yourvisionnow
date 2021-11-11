from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect


def index(request):
    """
    Old/beginning index view
    """
    return HttpResponse('Go to <a href="./kiosk">Kiosk</a> or \
                        Log In using <a href="./accounts/google/login">Google</a> \
                        <br /> or Log Out <a href="./accounts/logout">Here</a>.')


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


class CustomPlaceholder404(TemplateView):
    """
    Simplified Kiosk mode
    """
    template_name = '404.html'
