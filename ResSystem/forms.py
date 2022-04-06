from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class RoomForm(forms.ModelForm):
	class Meta:
		model = Room
		fields= '__all__'

class AgentForm(UserCreationForm):
    firstname = forms.CharField(max_length= 100)
    lastname = forms.CharField(max_length= 100)
    phone_number = forms.CharField(max_length=11)
    email = forms.EmailField()
    class Meta:
        model = Agent
        fields =  ('firstname', 'lastname', 'phone_number', 'email', 'username', 'password1', 'password2' )