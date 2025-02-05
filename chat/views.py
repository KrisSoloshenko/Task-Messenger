from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib import messages
from rest_framework import viewsets

from .models import User, Room
from .forms import SignUpForm
from .serializers import *


# представление стартовой страницы для выбора комнаты
def index(request):
    rooms = Room.objects.all()
    user_rooms = []
    
    for r in rooms:
        if request.user in r.current_users.all():
            user_rooms.append(r)
    
    return render(request, 'chat/index.html', {
        'user_rooms': user_rooms,
    })

# представление для выхода из системы
@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect("/login")
    return render(request, 'registration/logout.html', {})

# представление для регистрации в системе
class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/login/'
    template_name = 'registration/signup.html'
    
# представление для редактирования профиля пользователя
class ProfileUser(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'avatar']
    context_object_name = 'post'
    queryset = User.objects.all()
    template_name = 'profile.html'
    success_url = "/"
    
# представление для создания чата
@login_required
def create_room_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        current_users = request.POST.getlist('current_users')

        if not current_users or len(current_users) < 1:
            messages.error(request, 'Для создания чата выберите хотя бы одного участника.')
            return redirect('room_create') 

        current_users.append(request.user.id)
        
        if name and current_users:
            room = Room.objects.create(name=name, host=request.user)
            room.current_users.set(current_users)
            return redirect('room', pk=room.pk)
    
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/create_room.html', {'users': users})


# представление для редактирования чата
class UpdateRoom(LoginRequiredMixin, UpdateView):
    model = Room
    fields = ['name', 'current_users', 'photo']
    context_object_name = 'update_room'
    queryset = Room.objects.all()
    template_name = 'chat/update_room.html'


# представление для удаления чата
class DeleteRoom(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'chat/delete_room.html'
    success_url = reverse_lazy('index')

# представление для создания приватного чата
@login_required
def create_private_room(request, pk):
    rooms = Room.objects.all()
    
    if request.user.is_authenticated:
        recipient = get_object_or_404(User, pk=pk)

        for room in rooms:
                current_users = room.current_users.all()
                if len(current_users) == 2 and (recipient in current_users and request.user in current_users):
                    return redirect('room', pk=room.pk)
        
        new_room = Room.objects.create(name=f"{request.user} и {recipient}", host=request.user)
        new_room.current_users.add(recipient, request.user)
        return redirect('room', pk=new_room.pk)
    else:
        return redirect('login')

# представление для страницы чата
@login_required
def room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    
    if request.user not in room.current_users.all():
        return redirect('index')
    
    messages = room.messages.order_by('created_at')
    len_messages = len(messages)
    last_messages = []
    
    if len_messages > 10:
        last_messages = messages[(len_messages-10):]
    
    return render(request, 'chat/room.html', {
        "room": room,
        'messages': messages,
        'room_name': room.name,
        'chat_id': room.id,
        'username': request.user.username,
        'current_users': room.current_users.all(),
        'last_messages': last_messages,
    })
    
@login_required  
def users_list_view(request):
    users_list = User.objects.exclude(id=request.user.id) 
    return render(request, 'chat/users_list.html', {'users': users_list})


# ViewSet чата для API
class RoomViewset(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

# ViewSet комнаты для API
class MessageViewset(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    