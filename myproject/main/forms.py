from django import forms
from .models import Language, Technology, TechnologyDetail

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name', 'photo', 'slug']
        labels = {
            'name':'Назва',
            'slug':'Слаг'
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
        }

class TechnologyForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = ['name', 'description', 'slug', 'category', 'lang']
        labels = {
            'name': 'Назва',
            'description':'Опис',
            'slug': 'Слаг',
            'category': 'Категорія',
            'lang': 'До якої мови програмування відноситься',
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'lang': forms.Select(attrs={'class':'form-control'}),
        }

class TechnologyDetailForm(forms.ModelForm):
    class Meta:
        model = TechnologyDetail
        fields = ['topic', 'photo', 'description', 'tech']
        labels = {
            'topic':'Назва теми',
            'description':'Опис',
            'tech':'Вибір до якої технології відноситься',
        }
        widgets = {
            'topic': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'tech': forms.Select(attrs={'class':'form-control'}),
        }