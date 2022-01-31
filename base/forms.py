from dataclasses import fields
from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import Room

# Create your forms here

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']      #? We don't want the user to change these fields
        

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']