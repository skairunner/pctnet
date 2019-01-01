from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse

from sanitize import sanitizeInput


# 2 to 10 people
class PrivateMessageGroup(models.Model):
    members = models.ManyToManyField(User, related_name='pmgroups')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pmgroups_owned')
    title = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('viewgroupmsg', args=[self.pk])


class PrivateMessage(models.Model):
    # only one parent for a PM
    parent = models.ForeignKey(PrivateMessageGroup, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    content_html = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        base = reverse('viewgroupmsg', args=[self.parent.pk])
        return f'{base}#msg{self.pk}'

    def save(self, *args, **kwargs):
        self.content_html = sanitizeInput(self.content)
        super().save(*args, **kwargs)
