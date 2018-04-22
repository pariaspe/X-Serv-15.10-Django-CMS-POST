from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context

from .models import Pages

# Create your views here.
FORM = """
    <form action="" method="POST">
        <label for="name">Pagina:</label><br>
        <input type="text" name="name" value=""/><br>
        <label for="name">Contenido:</label><br>
        <input type="text" name="page" value=""/><br>
        <input type="submit" value="Send">
    </form>
"""

FORM_EDIT = """
    <form action="" method="POST">
        <label for="name">Contenido:</label><br>
        <input type="text" name="page" value="{prueba}"/><br>
        <input type="submit" value="Send">
    </form>
"""

def get_log(is_logged_in, username):
    if is_logged_in:
        logged = '<p>Logged in as ' + username + '.</br>'
        logged += '<a href=http://localhost:8000/logout>Logout</a></p>'
    else:
        logged = '<p>Not logged in. <a href=http://localhost:8000/login>Login</a></p>'
    return logged

def add_page(is_logged_in, nombre, contenido):
    msg = ''
    if is_logged_in:
        page = Pages(name=nombre, page=contenido)
        if page.name != '':
            try:
                page.save()
            except IntegrityError:
                Pages.objects.filter(name=nombre).update(page=contenido)
                msg = 'Valor actualizado.'
    else:
        msg = 'Para crear o editar una pagina necesitas estar logeado.'
    return msg

@csrf_exempt
def barra(request):
    msg = ''
    if request.method == 'POST':
        msg = add_page(request.user.is_authenticated(), request.POST['name'], request.POST['page'])

    pages = Pages.objects.all()
    lista = 'Paginas guardadas:<ul>'
    for page in pages:
        lista += '<li><a href="' + page.name + '">' + page.name + '</a></li>'
    lista += '</ul>'
    answer = '<h1>Sistema de gestión de contenido</h1>'
    answer += lista + msg
    answer += '<p>' + FORM + '</p>'
    answer += get_log(request.user.is_authenticated(), request.user.username)
    return HttpResponse(answer)

@csrf_exempt
def annotated_barra(request):
    msg = ''
    if request.method == 'POST':
        msg = add_page(request.user.is_authenticated(), request.POST['name'], request.POST['page'])

    pages = Pages.objects.all()
    lista = 'Paginas guardadas:<ul>'
    for page in pages:
        lista += '<li><a href="' + page.name + '">' + page.name + '</a></li>'
    lista += '</ul>'
    title = '<h1>Sistema de gestión de contenido</h1>'
    content = lista + msg + '<p>' + FORM + '</p>'
    content += get_log(request.user.is_authenticated(), request.user.username)

    template = get_template("annotated.html")

    return HttpResponse(template.render(
            Context({'title': title,
            'content': content})))

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

def annotated_other(request, recurso):
    try:
        page = Pages.objects.get(name=recurso)
        content = '<p><a href="/">Inicio</a></p>'
        content += get_log(request.user.is_authenticated(), request.user.username)

        template = get_template("annotated.html")
        return HttpResponse(template.render(
                Context({'title': page.page,
                'content': content})))
    except Pages.DoesNotExist:
        answer = 'La pagina ' + recurso + ' no está guardada.'
        answer += '<p><a href="/">Inicio</a></p>'

        template = get_template("annotated.html")
        return HttpResponse(template.render(
                Context({'title': answer})))

@csrf_exempt
def edit(request, recurso):
    if not request.user.is_authenticated():
        answer = 'Tienes que estar logeado para editar contenido de las paginas.'
        answer += get_log(request.user.is_authenticated(), request.user.username)
        return HttpResponse(answer)
    try:
        page = Pages.objects.get(name=recurso)
    except Pages.DoesNotExist:
        answer = 'La pagina ' + recurso + ' no está guardada.'
        answer += '<p><a href="/">Inicio</a></p>'
        return HttpResponseNotFound(answer)

    if request.method == 'POST':
        msg = add_page(request.user.is_authenticated, recurso, request.POST['page'])
        form = FORM_EDIT.format(prueba=request.POST['page'])
    else:
        form = FORM_EDIT.format(prueba=page.page)

    answer = '<h1>Editando: ' + recurso + '</h1>'
    answer += '<p>' + form + '</p>'
    answer += get_log(request.user.is_authenticated(), request.user.username)
    return HttpResponse(answer)
