from django.db import models
from django.utils import timezone

class Skill(models.Model):
    """Model for skills/technologies"""
    name = models.CharField(max_length=100, unique=True)
    proficiency = models.IntegerField(
        help_text="Proficiency level (0-100)",
        default=50
    )
    category = models.CharField(
        max_length=50,
        choices=[
            ('frontend', 'Frontend'),
            ('backend', 'Backend'),
            ('database', 'Database'),
            ('tools', 'Tools & Others'),
        ],
        default='backend'
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Bootstrap icon class (e.g., bi-code-slash)"
    )
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        ordering = ['category', 'order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Project(models.Model):
    """Model for portfolio projects"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(
        max_length=200,
        help_text="Brief description for project cards"
    )
    image = models.ImageField(
        upload_to='projects/',
        blank=True,
        null=True,
        help_text="Project screenshot or thumbnail"
    )
    technologies = models.ManyToManyField(
        Skill,
        related_name='projects',
        blank=True
    )
    github_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(
        default=False,
        help_text="Display on homepage"
    )
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        ordering = ['-is_featured', 'order', '-created_date']
    
    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """Model for contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"