import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    tags = models.ManyToManyField(Tag, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def publish(self):
        self.status = 'published'
        self.published_at = timezone.now()
        self.save()


# Add this to the existing models.py file

class UserProfile(models.Model):
    USER_TYPES = (
        ('viewer', 'Viewer'),
        ('editor', 'Editor'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='viewer')
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"


# Add this to your existing models.py file

class APIKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='api_key')
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username}'s API Key"
    
    def save(self, *args, **kwargs):
        # Ensure only editors can have API keys
        if hasattr(self.user, 'profile') and self.user.profile.user_type == 'editor':
            super().save(*args, **kwargs)
        else:
            raise ValueError("Only editors can have API keys")
