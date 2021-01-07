from django.shortcuts import render
from django.http import HttpResponse

def index(request):

    return HttpResponse("hi")

def timer(request):

    request_context={}

    return render(request,'timer.html',request_context)

# Create your views here.
