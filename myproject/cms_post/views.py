from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound

from .models import Pages

# Create your views here.

def barra(request):
    pages = Pages.objects.all()
    lista = 'Paginas guardadas:<ul>'
    for page in pages:
        lista += '<li>' + page.name + '</li>'
    lista += '</lu>'

    answer = '<h1>Sistema de gestión de contenido</h1>'
    answer += lista
    return HttpResponse(answer)

def other(request, recurso):
    try:
        page = Pages.objects.get(name=recurso)
        return HttpResponse(page.page)
    except Pages.DoesNotExist:
        answer = 'La pagina ' + recurso + ' no está guardada.'
        return HttpResponseNotFound(answer)
