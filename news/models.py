from django.db import models
from django.utils.timezone import now

class FamilyNews(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100, default="Admin")

    def __str__(self):
        return self.title


class Notification(models.Model):
    message = models.CharField(max_length=255)
    date = models.DateField(default=now)  # planned date for the event

    def __str__(self):
        return f"{self.message} on {self.date}"
