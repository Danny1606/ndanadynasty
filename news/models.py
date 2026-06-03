from django.db import models

class Post(models.Model):
    author_name = models.CharField(max_length=100, default="Anonymous")
    content = models.TextField()
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author_name}: {self.content[:30]}"

    @property
    def author(self):
        return self.author_name

    def get_author_display(self):
        return self.author_name

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author_name = models.CharField(max_length=100, default="Anonymous")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author_name} on {self.post}"

    @property
    def author(self):
        return self.author_name

    def get_author_display(self):
        return self.author_name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="event_images/", blank=True, null=True)
    organizer_name = models.CharField(max_length=100, default="Guest")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_organizer_display(self):
        return self.organizer_name

class Like(models.Model):
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
    author_name = models.CharField(max_length=100, default="Guest")

    class Meta:
        unique_together = ("post", "author_name")

    def __str__(self):
        return f"{self.author_name} liked {self.post}"

class ActivityLog(models.Model):
    author_name = models.CharField(max_length=100, default="Guest")
    action = models.CharField(max_length=50)
    post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, blank=True, null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, blank=True, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_display_text(self):
        return f"{self.author_name} performed {self.action}"

    def __str__(self):
        return self.get_display_text()
