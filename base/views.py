from multiprocessing import context
from webbrowser import get
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required       #? This is a 'decorator'
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


from .models import Room, Topic, Message
from .forms import RoomForm, UserForm

# Create your views here.


def loginPage(request):
    page = 'login'   #? Just a random var name, for an if-else block on the user-registration page
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()     # All usernames are lowercase on this site
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
    
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
        #? This "logout taking in 'request' " will delete the sessionid token, thereby logging out the user
    return redirect('home')


def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
                #? We're saving the form, but freezing it in time here
                #? This is because, we want to be able to access the user that was created
                #* We do this to 'format' the data entered by the user, in case there are some mistakes
            
            user.username = user.username.lower()       # All usernames should be lowercase
            user.save()
            login(request,user)         #? Login the newly created user
            return redirect('home')     #? And then send them to the home page
        else:
            messages.error(request, 'An error occured during registration, please try again!!')
    
    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)
    

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
            # Returns the 'query: topic name' after ?q in the URL
            # This is the ?q=### added to the url, (should be common knowledge now)
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )       # topic, name and description: All three are fields in the Room model
    
    topics = Topic.objects.all()[0:5]
    
    room_count = rooms.count()
    
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )
    
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request,pk):
    room = Room.objects.get(id=pk)

    room_messages = room.message_set.all()
    
    participants = room.participants.all()
    
    if request.method == 'POST':
        message = Message.objects.create(   # Fill in the three required fields for a message model
            user = request.user,
            room = room,     # room variable is defined above
            body = request.POST.get('body')     # name="body" for the input field in the template
        )
        
        room.participants.add(request.user)
        return redirect('room', pk=room.id)     #? We want the page to fully reload after the POST request, to avoid any unknown errors

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)


def userProfile(request,pk):
    
    user = User.objects.get(id=pk)
    
    rooms = user.room_set.all()
    #? Remember, that we can get all the children of a specific object, by doing the model_name_set.all()
    
    room_messages = user.message_set.all()
    
    topics = Topic.objects.all()
    
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    
    topics = Topic.objects.all()
    
    if request.method == 'POST':
        # print(request.POST)     #? request.POST is the 'query/list' containg the form data filled by the user
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        # form = RoomForm(request.POST)
        
        Room.objects.create(
            host=request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')
    
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user    #? The host should be added automatically, depending on which user created the room
        #     room.save()
        #     return redirect('home') # We can enter 'home' instead of absolute path, because of name="home" in urls.py
    
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)   #? So that the form is pre-filled with the current values
    topics = Topic.objects.all()
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!')
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        
        # form = RoomForm(request.POST, instance=room)
        #     #? If we don't specify instance=room, it'll create a NEW room, instead of updating the values of the correct room
        # if form.is_valid():
        #     form.save()
        #     return redirect('home')
    
    context = {'form':form, 'topics': topics, 'room': room}
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


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('You are not allowed here!!!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj':message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    
    context = {'form':form}
    return render(request, 'base/update-user.html', context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    topics = Topic.objects.filter(name__icontains=q)
    
    return render (request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})