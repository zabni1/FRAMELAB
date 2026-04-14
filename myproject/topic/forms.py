from django import forms
from django.utils.text import slugify

from .models import Topic


class TopicCreateForm(forms.ModelForm):
    CHOICES = (('С++', 'С++'),
               ('С#', 'С#'),
               ('Python', 'Python'),
               ('JavaScript', 'JavaScript'),
               ('Java', 'Java'),
               ('PHP', 'PHP'),
               ('Ruby', 'Ruby'),
               ('Go', 'Go'),
               ('Rust', 'Rust'),
               ('Немає категорії', 'Немає категорії'))

    category = forms.ChoiceField(choices=CHOICES,label="Категорія",widget=forms.Select(attrs={'class': 'form-control',
                                                                                              'placeholder':'Виберіть категорію'}))
    class Meta:
        model = Topic
        fields = ('title', 'description')

        labels = {
            'title':'Заголовок',
            'description':'Опис',

        }
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Введіть заголовок'}),
            'description': forms.TextInput(attrs={'class':'form-control','placeholder':'Введіть опис'}),
        }

        def clean(self):
            cleaned_data = super().clean()
            title = cleaned_data.get("title")
            if title:
                cleaned_data["slug"] = slugify(title)
            return cleaned_data