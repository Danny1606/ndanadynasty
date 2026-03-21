from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "news"   # ensures Django knows this belongs to the 'news' app

    def __str__(self):
        return self.title
