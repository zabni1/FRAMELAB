from django.db import models
from django.urls import reverse


class Topic(models.Model):
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=100)
    email = models.EmailField()
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return f"Назва теми: {self.name}"

    def get_absolute_url(self):
        return reverse('topic_detail', kwargs={'show_detail': self.slug})


class Comment(models.Model):
    email = models.CharField(max_length=100)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Коментар: {self.comment}"


class Reply(models.Model):
      email = models.CharField(max_length=100)
      topic = models.ForeignKey('Topic', on_delete=models.CASCADE)
      comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
      created_at = models.DateTimeField(auto_now_add=True)
      reply_to = models.CharField(max_length=100, null=True, blank=True)

class Likes(models.Model):
      email = models.CharField(max_length=100)
      comment = models.ForeignKey('Comment', on_delete=models.CASCADE, blank=True, null=True)
      reply = models.ForeignKey('Reply', on_delete=models.CASCADE, blank=True, null=True)



