from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect


def index(request):
    return HttpResponse('Go to <a href="./kiosk">Kiosk</a> or \
                        Log In using <a href="./accounts/google/login">Google</a> \
                        <br /> or Log Out <a href="./accounts/logout">Here</a>.')


# class Kiosk(TemplateView):
#     """
#     Simplified Kiosk mode
#     """
#     template_name = 'kiosk.html'

class KioskPage(TemplateView):
    """
    First page at root - kiosk view
    """
    template_name = 'index_new.html'

    def post(self, request, *args, **kwargs):
        if 'x var' not in request.session:
            request.session['x var'] = request.POST.get("x var")
        return redirect('/some/url/')


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
