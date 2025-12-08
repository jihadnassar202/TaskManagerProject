from django import forms
from .models import Task
from django.utils import timezone
from django.core.exceptions import ValidationError



class TaskForm(forms.ModelForm):
    """
    Form used to create and update Task instances in the UI.
    """
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'assigned_to','due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
        }
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.localdate():
            raise ValidationError("Due date cannot be in the past.")
        return due_date
