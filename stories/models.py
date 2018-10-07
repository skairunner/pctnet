from django.db import models
from django.contrib.auth.models import User


class Story(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dateposted = models.DateField()
    worktext = models.TextField()
    worktitle = models.CharField(max_length=255)
    summary = models.TextField(max_length=1250)

    def __str__(self):
        return "[Story: %s]" % (self.worktitle,)
