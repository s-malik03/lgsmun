from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dashboards.models import CommitteeControl
from hashlib import sha256
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages


# Create your views here.
@login_required
def admin(request):
    if request.session['utype'] != 'admin':
        return HttpResponse('Access denied')
    committees = CommitteeControl.objects.values('committee')
    committee_matrix = []

    for c in committees:
        committee_matrix.append(c['committee'])

    request_context = {'committees': committee_matrix,'username':request.user.username}
    return render(request, 'menu/admin.html', request_context)

@login_required
def dais(request):
    if request.session['utype'] != 'dais':
        return HttpResponse('Access denied')
    request_context = {'username':request.user.username}
    return render(request, 'menu/dais.html', request_context)

@login_required
def delegate(request):
    request_context = {'username':request.user.username}
    return render(request, 'menu/delegate.html', request_context)

@login_required
def changepassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/menu/' + request.session['utype'])
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'menu/changepassword.html', {
        'form': form, 'username':request.user.username
    })


@login_required
def setpassword(request):
    newpw = request.POST["new_password"]
    cpw = request.POST["confirm_password"]
    if newpw != cpw:
        return redirect('/menu/changepassword')
    uinfo = request.user
    uinfo.password = newpw
    uinfo.save()
    request_context = {}
    return redirect('/menu/' + request.session['utype'])


@login_required
def adminjoinsession(request):
    request_context = {}
    request.session['committee'] = request.GET["committee"]
    request.session['country'] = 'Dais'
    return redirect('/dashboards/dais')


@login_required
def joinsession(request):
    request_context = {}
    if request.session['utype'] == 'delegate':
        return redirect('/dashboards/hub')
    else:
        return redirect('/dashboards/' + request.session['utype'])
