from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView


def index(request):
    return HttpResponse('Go to <a href="./kiosk">Kiosk</a> or \
                        Log In using <a href="./accounts/google/login">Google</a> \
                        <br /> or Log Out <a href="./accounts/logout">Here</a>.')


class Kiosk(TemplateView):
    """
    Simplified Kiosk mode
    """
    template_name = 'kiosk.html'


class WelcomePage(TemplateView):
    """
    First / Login page at root
    """
    template_name = 'index.html'
