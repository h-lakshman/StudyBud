from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "username doesnot exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "username and password deosnot exist")
    return render(request, 'base/login_register.html', {'page': page})


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(
                request, 'There is some error while registering, register again')
    return render(request, 'base/login_register.html', {'form': form})


def logoutPage(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q))
    topics = Topic.objects.all().order_by('name')[0:5]
    rooms_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__name__icontains=q))
    return render(request, 'base/home.html', {'rooms': rooms, 'topics': topics, 'rooms_count': rooms_count,
                                              'room_messages': room_messages})


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    room_messages = user.message_set.all()
    return render(request, 'base/profile.html', {'user': user, 'rooms': rooms,
                                                 'topics': topics, 'room_messages': room_messages})


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    participants_count = participants.count()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    return render(request, 'base/room.html', {'room': room, 'room_messages': room_messages, 'participants': participants, 'participants_count': participants_count})


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    return render(request, 'base/create-room.html', {'form': form, 'topics': topics})


@login_required(login_url='login')
def updateRoom(request, pk):
    room = get_object_or_404(Room, id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all
    if request.user != room.host:
        return HttpResponse("You're not allowed here")
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    return render(request, 'base/create-room.html', {'form': form, 'room': room, 'topics': topics})


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = get_object_or_404(Room, id=pk)
    if request.user != room.host:
        return HttpResponse("You're not allowed here")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete-room.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = get_object_or_404(Message, id=pk)
    if request.user != message.user:
        return HttpResponse("You're not allowed here")
    if request.method == 'POST':
        temp = message.room.id
        message.delete()
        return redirect('room', pk=temp)
    return render(request, 'base/delete-room.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    form = UserForm(instance=request.user)
    if request.method == 'POST':
        user = request.user
        form = UserForm(request.POST, instance=user)
        if form.is_valid:
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})
