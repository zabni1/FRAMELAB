from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q

from .models import User

class ProfileForm(forms.Form):
    email = forms.CharField(label='Email або логін', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                      'placeholder': 'Email або логін'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not get_user_model().objects.filter(Q(username=email) | Q(email=email)).exists():
            raise forms.ValidationError("Такого логіна не існує!")
        return email

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)
        if not user:
            raise forms.ValidationError("Неправильний пароль!")
        return password

class RegisterForm(forms.ModelForm):

    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'Логін'}))

    class Meta:
        model = User
        fields = ('full_name', 'username', 'email', 'password')
        labels = {
            'full_name': "Повне ім'я",
            'email': 'Email',
            'password': 'Пароль',
        }

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Повне ім'я"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
        }



    def clean_username(self):
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError("Такий логін вже існує!")
        elif username.istitle():
            raise forms.ValidationError("Логін має починатися з маленької")
        for a in username:
            if a.isupper():
                raise forms.ValidationError("Логін має містити тільки маленькі літери")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такий email вже існує!")
        elif not '@' in email:
            raise forms.ValidationError("Невірний email!")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise forms.ValidationError("Такий пароль занадто короткий!")
        elif len(password) == 0:
            raise forms.ValidationError("Введіть пароль!")
        elif not any(char.isalpha() for char in password):
            raise forms.ValidationError("Введіть літери!")
        return password




class ProfileUserForm(forms.ModelForm):
    email = forms.CharField(disabled=True, label="Email",
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ('email','username', 'full_name' , 'password','photo')
        labels = {
            'full_name': "Прізвище та ім'я",
            'username': 'Логін',
            'password': 'Пароль',
            'photo': ''
        }

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control','placeholder':"Прізвище та ім'я"}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логін'}),
            'password': forms.TextInput(attrs={'class': 'form-control','placeholder':'Пароль'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError("Такий логін вже існує!")
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if get_user_model().objects.filter(password=password).exists():
            return forms.ValidationError("Створіть новий пароль!")
        elif len(password) < 6:
            raise forms.ValidationError("Такий пароль занадто короткий!")
        return password