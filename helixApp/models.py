from django.db import models
from django.contrib.auth.models import User
class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    thumbs_up = models.PositiveIntegerField(default=0)
    thumbs_down = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
