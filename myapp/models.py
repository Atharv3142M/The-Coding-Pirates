from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User model
    title = models.CharField(max_length=255)  # Blog title
    content = models.TextField()  # Blog content (HTML from Quill)
    labels = models.CharField(max_length=255, blank=True, null=True)  # Optional labels/tags
    publish_date = models.DateField(blank=True, null=True)  # Allow null for drafts
    publish_time = models.TimeField(blank=True, null=True)  # Allow null for drafts
    permalink = models.CharField(max_length=255, unique=True, blank=True, null=True)  # Unique for SEO
    location = models.CharField(max_length=255, blank=True, null=True)  # Optional location
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-create timestamp

    class Meta:
        ordering = ['-created_at']  # Newest blogs first

    def __str__(self):
        return self.title
