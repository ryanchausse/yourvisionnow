from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Go to <a href='./kiosk'>Kiosk</a>")


def kiosk(request):
    return HttpResponse("Kiosk app - Your Vision Now")
