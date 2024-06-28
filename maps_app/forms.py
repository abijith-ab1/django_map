from django import forms
from .models import SearchHistory

class SearchForm(forms.ModelForm):
    search_term = forms.CharField(label='')

    class Meta:
        model = SearchHistory
        fields = ['search_term', ]
        widgets = {
            'search_term': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Search for a location',
                'id': 'location-input'
            })
        }
