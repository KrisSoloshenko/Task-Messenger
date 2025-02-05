from django.urls import path, include

from . import views
from .views import ProfileUser, UpdateRoom, DeleteRoom


urlpatterns = [
    path('', views.index, name="index"),
    path('profile/<int:pk>/', ProfileUser.as_view(), name='profile'),
    path('room/<int:pk>/', views.room, name='room'),
    path('room/create/', views.create_room_view, name='room_create'),
    path('room/<int:pk>/update/', UpdateRoom.as_view(), name='update_room'),
    path('room/<int:pk>/delete/', DeleteRoom.as_view(), name='delete_room'),
    path('users_list/', views.users_list_view, name='users_list'),
    path('private_room/<int:pk>/', views.create_private_room, name='private_room')
]
