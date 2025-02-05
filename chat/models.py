from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse


class User(AbstractUser):
    """создана кастомная модель User, обращение к модели get_user_model()"""
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True, verbose_name="фотография", default="avatar/default.png")


class Room(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True, verbose_name="название чата")
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rooms')
    current_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='current_rooms', verbose_name="участники")
    photo = models.ImageField(upload_to='room/', null=True, blank=True, verbose_name="фотография")
    
    def __str__(self):
        return f"Room ({self.name}, {self.host})"
    
    def get_absolute_url(self):
        return reverse('room', args=[str(self.id)])


class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages',)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('created_at',)
        
    def __str__(self):
        return f"Message ({self.user}, {self.room})"