from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User, Room


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
        )
        

class ChatForm(forms.ModelForm):
    current_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple, 
        required=False
    )

    class Meta:
        model = Room
        fields = ['name', 'current_users',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }