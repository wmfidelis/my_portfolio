from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import DailyCheckIn, GratitudeEntry, MeditationSession, CommunityPost

class DailyCheckInForm(forms.ModelForm):
    """Form for daily check-in"""
    
    class Meta:
        model = DailyCheckIn
        fields = ['morning_mood', 'evening_mood', 'prayed', 'meditated', 
                  'read_scripture', 'meditation_minutes', 'notes']
        widgets = {
            'morning_mood': forms.RadioSelect(),
            'evening_mood': forms.RadioSelect(),
            'notes': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Any reflections or thoughts for today...',
                'class': 'form-control'
            }),
            'meditation_minutes': forms.NumberInput(attrs={
                'min': 0,
                'class': 'form-control',
                'placeholder': 'Minutes'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'morning_mood',
            'evening_mood',
            Row(
                Column(Field('prayed', css_class='form-check-input'), css_class='col-md-4'),
                Column(Field('meditated', css_class='form-check-input'), css_class='col-md-4'),
                Column(Field('read_scripture', css_class='form-check-input'), css_class='col-md-4'),
            ),
            'meditation_minutes',
            'notes',
            Submit('submit', 'Save Check-In', css_class='btn btn-primary btn-lg mt-3')
        )


class GratitudeEntryForm(forms.ModelForm):
    """Form for gratitude journal entries"""
    
    class Meta:
        model = GratitudeEntry
        fields = ['entry']
        widgets = {
            'entry': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'What are you grateful for today? List at least 3 things...',
                'class': 'form-control'
            })
        }
        labels = {
            'entry': 'Today I am grateful for...'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'entry',
            Submit('submit', 'Save Gratitude Entry', css_class='btn btn-success btn-lg mt-3')
        )


class MeditationSessionForm(forms.ModelForm):
    """Form for logging meditation/prayer sessions"""
    
    class Meta:
        model = MeditationSession
        fields = ['session_type', 'duration_minutes', 'notes']
        widgets = {
            'session_type': forms.Select(attrs={'class': 'form-select'}),
            'duration_minutes': forms.NumberInput(attrs={
                'min': 1,
                'class': 'form-control',
                'placeholder': 'Duration in minutes'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Any insights or reflections...',
                'class': 'form-control'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'session_type',
            'duration_minutes',
            'notes',
            Submit('submit', 'Log Session', css_class='btn btn-primary mt-3')
        )


class CommunityPostForm(forms.ModelForm):
    """Form for community encouragement posts"""
    
    class Meta:
        model = CommunityPost
        fields = ['content', 'display_name', 'is_anonymous']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Share your encouragement, testimony, or words of hope...',
                'class': 'form-control'
            }),
            'display_name': forms.TextInput(attrs={
                'placeholder': 'How do you want to appear? (optional)',
                'class': 'form-control'
            })
        }
        labels = {
            'content': 'Your Message',
            'display_name': 'Display Name',
            'is_anonymous': 'Post Anonymously'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'content',
            Row(
                Column('display_name', css_class='col-md-8'),
                Column(Field('is_anonymous', css_class='form-check-input'), css_class='col-md-4'),
            ),
            Submit('submit', 'Share Encouragement', css_class='btn btn-success btn-lg mt-3')
        )