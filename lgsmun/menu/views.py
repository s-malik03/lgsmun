from django.shortcuts import render
from login.models import User

# Create your views here.

def admin(request):
    if request.session['utype']!='admin':
        return HttpResponse('Access denied')
    request_context={}
    return render(request,'menu/admin.html',request_context)

def dais(request):
    if request.session['utype']!='dais':
        return HttpResponse('Access denied')
    request_context={}
    return render(request,'menu/dais.html',request_context)

def delegate(request):

    request_context={}
    return render(request,'menu/delegate.html',request_context)

def changepassword(request):

    request_context={}
    return HttpResponse("")

def adminjoinsession(request):

    request_context={}
    return HttpResponse("")

def joinsession(request):

    request_context={}
    return HttpResponse("")
