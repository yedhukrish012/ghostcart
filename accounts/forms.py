from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from . models import Account, AddressBook


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
    code = forms.CharField(
        max_length=8,
        required=True,
        help_text='Enter code',
        widget=forms.TextInput(attrs={'class': 'custom-class', 'placeholder': 'Enter code here'})
    )

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("email", "phone_number")
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "8606615693"}),
        }
  

class AddressBookForm(forms.ModelForm):
    # address =forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-1', 'placeholder':'Enter Address'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Last Name'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Phone Number'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'E-mail'}))
    address_line_1 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'House No & Locality'}))
    address_line_2 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Address line 2(optional)'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'City'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'State'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Country'}))
    pincode = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Pincode'}))
    status = forms.BooleanField(required=False,widget=forms.CheckboxInput())
    
    class Meta:
        model = AddressBook
        # fields = ['first_name','last_name','phone','email','address_line_1','address_line_2','city','state','country','pincode','status']
        exclude = ("user",)