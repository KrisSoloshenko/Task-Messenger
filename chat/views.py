from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout

from .models import User
from .forms import SignUpForm


def index(request):
    return render(request, "chat/index.html")


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect("/login")
    return render(request, 'registration/logout.html', {})


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/login/'
    template_name = 'registration/signup.html'
    

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'avatar']
    context_object_name = 'post'
    queryset = User.objects.all()
    template_name = 'profile.html'
    success_url = "/"
