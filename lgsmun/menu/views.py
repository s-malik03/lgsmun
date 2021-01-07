from django.shortcuts import render,redirect
from login.models import User
from hashlib import sha256

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

    return render(request,'menu/changepassword.html',request_context)

def setpassword(request):

    newpw=request.POST["new_password"]
    uinfo=User.objects.get(email=request.session['uid'])
    uinfo.password=sha256(newpw.encode('utf-8')).hexdigest()
    uinfo.save()
    request_context={}
    return redirect('/menu/'+request.session['utype'])

def adminjoinsession(request):

    request_context={}
    return HttpResponse("")

def joinsession(request):

    request_context={}
    return HttpResponse("")
