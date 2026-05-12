from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name        = models.CharField(max_length=100)
    slug        = models.SlugField(unique=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Thread(models.Model):
    title    = models.CharField(max_length=255)
    content  = models.TextField(help_text="The main post content.")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='threads')
    symbol   = models.CharField(max_length=20, blank=True, help_text="e.g., BTCUSDT, EURUSD, AAPL")
    author   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned  = models.BooleanField(default=False)
    is_locked  = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def reply_count(self):
        return self.replies.count()


class Reply(models.Model):
    thread    = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='replies')
    author    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    content   = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reply by {self.author.username} on {self.thread.title}"
