from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class List(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        )


class Todo(models.Model):
    content = models.TextField()
    given_list = models.ForeignKey(List, on_delete=models.CASCADE)