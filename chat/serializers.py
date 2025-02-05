from .models import Room, Message
from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
        
class RoomSerializer(serializers.ModelSerializer): 
    # host = UserSerializer(read_only = True)
    # current_users = UserSerializer(many=True, read_only=True)\
    photo = serializers.ImageField(use_url='room/', required=False)

    class Meta:
        model = Room
        fields = ["id", "name", "host", "current_users", "photo"]
    
    
class MessageSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    # room = RoomSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'room', 'user', 'text', 'created_at']
        