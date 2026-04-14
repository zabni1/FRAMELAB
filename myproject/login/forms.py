from django import forms
from django.contrib.auth import get_user_model


class LoginForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
        labels = {
            'email': 'Email або логін',
            'password': 'Пароль',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email або логін'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        }



class RegisterForm(forms.Form):
    full_name = forms.CharField(label="Повне ім'я",widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                 'placeholder': "Повне ім'я"}))
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'Логін'}))

    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                          'placeholder': 'Email'}))

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                'placeholder': 'Пароль'}))




    # class Meta:
    #     model = get_user_model()
    #     fields = ('full_name','username','email', 'password')
    #     labels = {
    #         'full_name': "Повне ім'я",
    #         'username': 'Логін',
    #         'email': 'Email',
    #         'password': 'Пароль',
    #     }
    #     widgets = {
    #         'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Повне ім'я"}),
    #         'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логін'}),
    #         'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    #         'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
    #     }

    def clean_username(self):
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError("Такий логін вже існує!")
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