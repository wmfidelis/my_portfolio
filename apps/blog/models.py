from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from my_portfolio.settings import supabase  # import the client
import os


class Category(models.Model):
    """Blog post categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:category_posts', kwargs={'slug': self.slug})


class Tag(models.Model):
    """Blog post tags"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:tag_posts', kwargs={'slug': self.slug})


class Post(models.Model):
    """Blog post model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts',default=1)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='posts'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    content = models.TextField()
    excerpt = models.TextField(
        max_length=300,
        blank=True,
        help_text="Brief description for post previews"
    )
    featured_image = models.ImageField(
        upload_to='blog/images/',
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Display on homepage"
    )
    views = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-published_date', '-created_date']
        indexes = [
            models.Index(fields=['-published_date']),
            models.Index(fields=['status']),
        ]
    

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Ensure slug is unique across all posts
            while Post.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        if self.status == 'published' and not self.published_date:
            self.published_date = timezone.now()

        if not self.excerpt and self.content:
            self.excerpt = self.content[:297] + '...' if len(self.content) > 300 else self.content

        super().save(*args, **kwargs)
        
        if self.featured_image:
            file_path = self.featured_image.name           
            # Check if file already exists in Supabase
            try:
                supabase.storage.from_("media").upload(
            file_path, 
            open(self.featured_image.path, "rb").read()
        )
                
            except Exception as e:
                print("Supabase upload error:", e)
            
            # Optional: remove local file after upload
            if os.path.exists(self.featured_image.path):
                os.remove(self.featured_image.path)

    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        """Increment post view count"""
        self.views += 1
        self.save(update_fields=['views'])
    
    @property
    def reading_time(self):
        """Calculate estimated reading time in minutes"""
        words_per_minute = 200
        word_count = len(self.content.split())
        minutes = word_count / words_per_minute
        return max(1, round(minutes))


class Comment(models.Model):
    """Blog post comments"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments')
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    
    class Meta:
        ordering = ['created_date']
    
    def __str__(self):
        return f'{self.author.username} on {self.post.title}'
    
    @property
    def is_reply(self):
        return self.parent is not None