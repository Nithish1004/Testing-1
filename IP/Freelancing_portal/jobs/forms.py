from django import forms
from jobs.models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'budget']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'border rounded-lg w-full p-2'}),
            'description': forms.Textarea(attrs={'class': 'border rounded-lg w-full p-2', 'rows': 4}),
            'budget': forms.NumberInput(attrs={'class': 'border rounded-lg w-full p-2'}),
        }
