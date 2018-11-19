from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify


class Story(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    datefirstposted = models.DateField()
    datelastposted = models.DateField()
    worksummary = models.TextField(max_length=1250)
    worktitle = models.CharField(max_length=255)
    slug = models.SlugField(default="")
    firstchapter_id = models.IntegerField(default=-1)

    def __str__(self):
        return f"[Story: {self.worktitle}]"

    def get_absolute_url(self):
        return reverse("viewstory", args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.worktitle)
        super(Story, self).save(*args, **kwargs)


class Chapter(models.Model):
    parent = models.ForeignKey(Story, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    chapterorder = models.IntegerField(default=0)
    dateposted = models.DateField()
    chaptertext = models.TextField()
    chaptertitle = models.CharField(max_length=255)
    slug = models.SlugField(default="")
    chaptersummary = models.TextField(max_length=1250)

    def __str__(self):
        return f"[Chapter: {self.parent.worktitle}--{self.chaptertitle}]"

    def get_absolute_url(self):
        return reverse("chapter-only-view",
                       args=[self.id])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.chaptertitle)
        super(Chapter, self).save(*args, **kwargs)
