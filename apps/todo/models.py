from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Task(models.Model):
    """Task model for todo items"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, help_text="Optional task details")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='todo'
    )
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Optional deadline for the task"
    )
    completed_date = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['due_date']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('todo:task_detail', kwargs={'pk': self.pk})
    
    def mark_complete(self):
        """Mark task as completed"""
        self.status = 'completed'
        self.completed_date = timezone.now()
        self.save()
    
    def mark_incomplete(self):
        """Mark task as incomplete"""
        self.status = 'todo'
        self.completed_date = None
        self.save()
    
    @property
    def is_overdue(self):
        """Check if task is overdue"""
        if self.due_date and self.status != 'completed':
            return timezone.now() > self.due_date
        return False
    
    @property
    def is_due_soon(self):
        """Check if task is due within 24 hours"""
        if self.due_date and self.status != 'completed':
            time_until_due = self.due_date - timezone.now()
            return timezone.timedelta(0) < time_until_due <= timezone.timedelta(hours=24)
        return False
    
    @property
    def priority_class(self):
        """Return Bootstrap class based on priority"""
        priority_classes = {
            'low': 'secondary',
            'medium': 'info',
            'high': 'warning',
            'urgent': 'danger',
        }
        return priority_classes.get(self.priority, 'secondary')
    
    @property
    def status_class(self):
        """Return Bootstrap class based on status"""
        status_classes = {
            'todo': 'secondary',
            'in_progress': 'primary',
            'completed': 'success',
        }
        return status_classes.get(self.status, 'secondary')