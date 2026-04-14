from django.db import models

class Message(models.Model):
    user1 = models.IntegerField()
    user2 = models.IntegerField()
    message = models.TextField(max_length=500, blank=False, null=False)

    def __str__(self):
        return self.message