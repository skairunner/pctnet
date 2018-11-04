from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify


class Story(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dateposted = models.DateField()
    worktext = models.TextField()
    worktitle = models.CharField(max_length=255)
    summary = models.TextField(max_length=1250)
    slug = models.SlugField(default="")

    def __str__(self):
        return "[Story: %s]" % (self.worktitle,)

    def get_absolute_url(self):
        return reverse("viewstory", args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.worktitle)
        super(Story, self).save(*args, **kwargs)
