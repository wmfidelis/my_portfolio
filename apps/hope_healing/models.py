from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class MoodCategory(models.Model):
    """Categories for mood tracking"""
    MOOD_CHOICES = [
        ('great', 'Great 😊'),
        ('good', 'Good 🙂'),
        ('okay', 'Okay 😐'),
        ('struggling', 'Struggling 😔'),
        ('difficult', 'Very Difficult 😢'),
    ]
    
    name = models.CharField(max_length=20, choices=MOOD_CHOICES, unique=True)
    color = models.CharField(max_length=20, default='primary')
    
    class Meta:
        verbose_name_plural = 'Mood Categories'
    
    def __str__(self):
        return self.get_name_display()


class DailyCheckIn(models.Model):
    """Daily mood and spiritual practice tracking"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_checkins')
    date = models.DateField(default=timezone.now)
    
    # Mood tracking
    morning_mood = models.CharField(
        max_length=20,
        choices=MoodCategory.MOOD_CHOICES,
        blank=True,
        help_text="How are you feeling this morning?"
    )
    evening_mood = models.CharField(
        max_length=20,
        choices=MoodCategory.MOOD_CHOICES,
        blank=True,
        help_text="How are you feeling this evening?"
    )
    
    # Spiritual practices
    prayed = models.BooleanField(default=False, help_text="Did you pray today?")
    meditated = models.BooleanField(default=False, help_text="Did you meditate today?")
    read_scripture = models.BooleanField(default=False, help_text="Did you read spiritual texts?")
    
    # Meditation/prayer duration in minutes
    meditation_minutes = models.PositiveIntegerField(default=0)
    
    # Notes
    notes = models.TextField(blank=True, help_text="Any reflections for today?")
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']
        indexes = [
            models.Index(fields=['user', '-date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"


class AffirmationCategory(models.Model):
    """Categories for affirmations"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name_plural = 'Affirmation Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Affirmation(models.Model):
    """Affirmations for different needs"""
    text = models.TextField()
    category = models.ForeignKey(
        AffirmationCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='affirmations'
    )
    author = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['?']  # Random ordering for variety
    
    def __str__(self):
        return self.text[:50] + ('...' if len(self.text) > 50 else '')


class GratitudeEntry(models.Model):
    """Daily gratitude journal entries"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gratitude_entries')
    date = models.DateField(default=timezone.now)
    entry = models.TextField(help_text="What are you grateful for today?")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Gratitude Entries'
        ordering = ['-date']
        indexes = [
            models.Index(fields=['user', '-date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"


class MeditationSession(models.Model):
    """Track meditation/prayer sessions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meditation_sessions')
    session_type = models.CharField(
        max_length=20,
        choices=[
            ('meditation', 'Meditation'),
            ('prayer', 'Prayer'),
            ('breathing', 'Breathing Exercise'),
        ],
        default='meditation'
    )
    duration_minutes = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['user', '-date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_session_type_display()} ({self.duration_minutes}min)"


class Resource(models.Model):
    """Mental health and spiritual resources"""
    RESOURCE_TYPES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('book', 'Book'),
        ('website', 'Website'),
        ('hotline', 'Crisis Hotline'),
        ('app', 'Mobile App'),
    ]
    
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    description = models.TextField()
    url = models.URLField(blank=True)
    phone = models.CharField(max_length=50, blank=True, help_text="For hotlines")
    is_crisis_support = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_crisis_support', '-is_featured', 'title']
    
    def __str__(self):
        return self.title


class CommunityPost(models.Model):
    """Anonymous community encouragement posts"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_posts')
    display_name = models.CharField(
        max_length=50,
        default='Anonymous',
        help_text="How you want to appear (optional)"
    )
    content = models.TextField()
    is_anonymous = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=True)
    likes_count = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['-created_date']),
        ]
    
    def __str__(self):
        author_name = self.display_name if self.is_anonymous else self.author.username
        return f"{author_name}: {self.content[:50]}"


class CommunityPostLike(models.Model):
    """Track likes on community posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='likes')
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'post']
    
    def __str__(self):
        return f"{self.user.username} liked post {self.post.id}"