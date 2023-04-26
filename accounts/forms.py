from django import forms
from . models import Account


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