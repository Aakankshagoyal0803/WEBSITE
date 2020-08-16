from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class orderform(forms.ModelForm):
    class Meta:
        model=order
        fields='__all__' #or use list
        #to get all fields of order class

class customerform(forms.ModelForm):
    class Meta:
        model=customer
        fields='__all__'

class customer_formacc(forms.ModelForm):
    class Meta:
        model=customer
        fields='__all__'
        exclude=['user']

class createuserform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
