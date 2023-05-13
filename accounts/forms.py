from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from . models import Account, UserProfile


class registration(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'John'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Doe'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'johndoe@abc.com'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'xxxxxxxxxx'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-2', 'placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-2', 'placeholder':'Confirm Password'}))
    class Meta:
        model = Account
        fields = ['first_name','last_name','email','phone_number','password1','password2']

    def clean(self):
        cleaned_data = super(registration, self).clean()
        password1 = cleaned_data.get('password1') 
        password2 = cleaned_data.get('password2')  

        if password1 != password2:
            raise forms.ValidationError("Password and confirm password don't match!")

class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code')

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("first_name","last_name","phone_number")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", 'placeholder':'8606615693'}),
        }

  
class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False,error_messages= {'invalid':("image file only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ("address_line1","address_line2","city","state","country","profile_picture")
        widgets = {
            "address_line1": forms.TextInput(attrs={"class": "form-control", 'placeholder':'dude'}),
            "address_line2": forms.TextInput(attrs={"class": "form-control", 'placeholder':'Deo'}),
            "city": forms.TextInput(attrs={"class": "form-control", 'placeholder':'Alappuzha'}),
            "state": forms.TextInput(attrs={"class": "form-control", 'placeholder':'Kerala'}),
            "country": forms.TextInput(attrs={"class": "form-control", 'placeholder':'India'}),
            "profile_picture": forms.FileInput(attrs={"class": "form-control-file"}),
        }