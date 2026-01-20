from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import Task

class TaskForm(forms.ModelForm):
    """Form for creating and editing tasks"""
    
    due_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        help_text="Optional deadline for the task"
    )
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter task title',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Add task details (optional)',
                'rows': 4,
                'class': 'form-control'
            }),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'title',
            'description',
            Row(
                Column('priority', css_class='form-group col-md-6 mb-3'),
                Column('status', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'due_date',
            Submit('submit', 'Save Task', css_class='btn btn-primary btn-lg mt-3')
        )


class TaskFilterForm(forms.Form):
    """Form for filtering tasks"""
    STATUS_CHOICES = [('', 'All Status')] + list(Task.STATUS_CHOICES)
    PRIORITY_CHOICES = [('', 'All Priorities')] + list(Task.PRIORITY_CHOICES)
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search tasks...',
            'class': 'form-control'
        })
    )
    status = forms.ChoiceField(
        required=False,
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    priority = forms.ChoiceField(
        required=False,
        choices=PRIORITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Default (Newest First)'),
            ('due_date', 'Due Date'),
            ('priority', 'Priority'),
            ('title', 'Title (A-Z)'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )