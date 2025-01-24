from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
 
from chat.models import User, Message, Room
 
admin.site.register(User, UserAdmin)
admin.site.register(Message)
admin.site.register(Room)
