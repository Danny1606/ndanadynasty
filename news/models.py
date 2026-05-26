from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pin = models.CharField(max_length=4, unique=True)
    picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    unit = models.CharField(max_length=100, blank=True, null=True, help_text="Family unit or location (e.g., 'Unit A', 'Main House')")

    def __str__(self):
        return self.username
    
    def get_display_name(self):
        """Return user's full name with unit"""
        full_name = self.get_full_name() or self.username
        if self.unit:
            return f"{full_name} ({self.unit})"
        return full_name


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    author_name = models.CharField(max_length=100, default="Anonymous", blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_author_display(self):
        return self.author.username if self.author else self.author_name

    def __str__(self):
        return f"{self.get_author_display()} - {self.content[:30]}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    author_name = models.CharField(max_length=100, default="Anonymous", blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_author_display(self):
        return self.author.username if self.author else self.author_name

    def __str__(self):
        return f"{self.get_author_display()} on {self.post.id}"


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Prevent duplicate likes

    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"


class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_events", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.title} ({self.date})"


class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('post', 'Created a post'),
        ('comment', 'Posted a comment'),
        ('like', 'Liked a post'),
        ('event', 'Created an event'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="activity_logs")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def get_display_text(self):
        """Generate readable activity text with user name and unit"""
        user_display = self.user.get_display_name()
        if self.action == 'post':
            return f"{user_display} shared a post"
        elif self.action == 'comment':
            return f"{user_display} commented on a post"
        elif self.action == 'like':
            return f"{user_display} liked a post"
        elif self.action == 'event':
            return f"{user_display} created an event"
        return user_display
    
    def __str__(self):
        return f"{self.get_display_text()} at {self.timestamp}"
