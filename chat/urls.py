from django.urls import path

from . import views
from .views import ProfileUser


urlpatterns = [
    path("", views.index, name="index"),
    path('profile/<int:pk>/', ProfileUser.as_view(), name='profile'),
]
