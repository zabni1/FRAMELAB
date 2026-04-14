from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {
            'message': '',
        }
        widgets = {
            'message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть запит'}),
        }