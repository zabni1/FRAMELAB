from django import forms

class QueryForm(forms.Form):
      query = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Пошук'}))