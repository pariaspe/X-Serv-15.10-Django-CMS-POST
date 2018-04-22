from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound

from .models import Pages

# Create your views here.
def get_log(is_logged_in, username):
    if is_logged_in:
        logged = '<p>Logged in as ' + username + '.</br>'
        logged += '<a href=logout>Logout</a></p>'
    else:
        logged = '<p>Not logged in. <a href=login>Login</a></p>'
    return logged

def barra(request):
    pages = Pages.objects.all()
    lista = 'Paginas guardadas:<ul>'
    for page in pages:
        lista += '<li><a href="' + page.name + '">' + page.name + '</a></li>'
    lista += '</lu>'
    answer = '<h1>Sistema de gestión de contenido</h1>'
    answer += lista
    answer += get_log(request.user.is_authenticated(), request.user.username)
    return HttpResponse(answer)

def other(request, recurso):
    try:
        page = Pages.objects.get(name=recurso)
        answer = page.page + '<p><a href="/">Inicio</a></p>'
        answer += get_log(request.user.is_authenticated(), request.user.username)
        return HttpResponse(answer)
    except Pages.DoesNotExist:
        answer = 'La pagina ' + recurso + ' no está guardada.'
        answer += '<p><a href="/">Inicio</a></p>'
        return HttpResponseNotFound(answer)
