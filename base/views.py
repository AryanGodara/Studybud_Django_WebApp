from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required       #? This is a 'decorator'
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


from .models import Room, Topic
from .forms import RoomForm

# Create your views here.


def loginPage(request):
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password does not exist')
    
    context = {}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
        #? This "logout taking in 'request' " will delete the sessionid token, thereby logging out the user
    return redirect('home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
            # Returns the 'query: topic name' after ?q in the URL
            # This is the ?q=### added to the url, (should be common knowledge now)
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )       # topic, name and description: All three are fields in the Room model
    
    topics = Topic.objects.all()
    
    room_count = rooms.count()
    
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)


def room(request,pk):
    room = Room.objects.get(id=pk)

    context = {'room': room}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    
    if request.method == 'POST':
        # print(request.POST)     #? request.POST is the 'query/list' containg the form data filled by the user
        form = RoomForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('home') # We can enter 'home' instead of absolute path, because of name="home" in urls.py
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)   #? So that the form is pre-filled with the current values
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!')
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
            #? If we don't specify instance=room, it'll create a NEW room, instead of updating the values of the correct room
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj':room})