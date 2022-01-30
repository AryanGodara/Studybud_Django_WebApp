from django.shortcuts import render

# Create your views here.

rooms = [
    {'id': 1, 'name': 'Lets Learn Python'},
    {'id': 2, 'name': 'Design with me'},
    {'id': 3, 'name': 'Fronted Developer'},
]

def home(request):
    context = {'rooms':rooms}
    return render(request, 'base/home.html', context)

def room(request,pk):
    return render(request, 'base/room.html')