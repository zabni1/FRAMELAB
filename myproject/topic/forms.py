from django import forms
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


    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) > 100:
            raise forms.ValidationError("Такий заголовок занадто довгий")
        return title

    def clean_description(self):
        description = self.cleaned_data["description"]
        if len(description) > 1000:
            raise forms.ValidationError("Такий опис занадто довгий")
        return description