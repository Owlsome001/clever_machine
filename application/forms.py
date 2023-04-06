from django import forms
from application.models import Project,User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields =["name"]

class RegisterForm(UserCreationForm):

    class Meta:
        model= User
        fields = ['username','password1', 'password2']


      