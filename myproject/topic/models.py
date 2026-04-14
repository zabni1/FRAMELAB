from django.db import models
from django.urls import reverse


class Topic(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    email = models.EmailField()
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return f"Назва теми: {self.title}"

    def get_absolute_url(self):
        return reverse('topic_detail', kwargs={'show_detail': self.slug})


class Comment(models.Model):
    comment = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)

    def __str__(self):
        return f"Коментар: {self.comment}"


class Reply(models.Model):
      username = models.CharField(max_length=100)
      email = models.CharField(max_length=100)
      reply = models.CharField(max_length=500)
      comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='replies')
      created_at = models.DateTimeField(auto_now_add=True)
      reply_to = models.CharField(max_length=100, null=True, blank=True)

class Likes(models.Model):
      email = models.CharField(max_length=100)
      comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='likes', blank=True, null=True)
      reply = models.ForeignKey('Reply', on_delete=models.CASCADE, blank=True, null=True)



