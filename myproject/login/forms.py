from django import forms
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
        labels = {
            'email': 'Email',
            'password': 'Password',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }


class RegisterForm(forms.Form):
    class Meta:
        model = get_user_model()
        fields = ('full_name','email', 'password')
        labels = {
            'full_name': 'Full Name',
            'email': 'Email',
            'password': 'Password',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }


class ProfileUserForm(forms.ModelForm):
    email = forms.CharField(disabled=True, label="Email",
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ('email', 'full_name' , 'password','photo')
        labels = {
            'full_name': "Прізвище та ім'я",
            'password': 'Пароль',
            'photo': ''


        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control','placeholder':"Прізвище та ім'я"}),
            'password': forms.TextInput(attrs={'class': 'form-control','placeholder':'Пароль'}),


        }