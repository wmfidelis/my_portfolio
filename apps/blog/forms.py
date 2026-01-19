from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import Post, Comment

class PostForm(forms.ModelForm):
    """Form for creating and editing blog posts"""
    
    class Meta:
        model = Post
        fields = [
            'title', 'category', 'tags', 'content', 'excerpt',
            'featured_image', 'status', 'is_featured'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter post title',
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your post content here...',
                'rows': 15,
                'class': 'form-control'
            }),
            'excerpt': forms.Textarea(attrs={
                'placeholder': 'Brief description (max 300 characters)',
                'rows': 3,
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.CheckboxSelectMultiple(),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            'title',
            Row(
                Column('category', css_class='form-group col-md-6 mb-3'),
                Column('status', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'content',
            'excerpt',
            'tags',
            'featured_image',
            Field('is_featured', css_class='form-check-input'),
            Submit('submit', 'Save Post', css_class='btn btn-primary btn-lg mt-3')
        )


class CommentForm(forms.ModelForm):
    """Form for posting comments"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Share your thoughts...',
                'rows': 4,
                'class': 'form-control'
            })
        }
        labels = {
            'content': 'Comment'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'content',
            Submit('submit', 'Post Comment', css_class='btn btn-primary mt-2')
        )


class PostSearchForm(forms.Form):
    """Search form for blog posts"""
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search posts...',
            'class': 'form-control'
        })
    )
    category = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Category
        self.fields['category'].queryset = Category.objects.all()