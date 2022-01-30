from django.shortcuts import render

# Create your views here.

def home(request):
    return HttpResponse('Home Page')
def room(request):
    return HttpResponse('Room')