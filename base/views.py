from multiprocessing import context
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
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
            break

    context = {'room': room}
    return render(request, 'base/room.html', context)