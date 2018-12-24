from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.shortcuts import redirect

from sanitize import sanitizeInput, sanitizeMarkdown


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
    # chapters may be rearranged
    chapterorder = models.IntegerField(default=0)
    dateposted = models.DateField()
    chaptertext = models.TextField()
    chaptertext_html = models.TextField(default='')
    chaptertitle = models.CharField(max_length=255)
    slug = models.SlugField(default="")
    chaptersummary = models.TextField(max_length=1250, default='', blank=True)
    chaptersummary_html = models.TextField(default='')

    def __str__(self):
        return f"[Chapter: {self.parent.worktitle}--{self.chaptertitle}]"

    def get_absolute_url(self):
        slug = f'{self.parent.slug}.{self.slug}'
        return reverse('viewchapter',
                       args=[self.parent.pk, self.pk, slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.chaptertitle)
        self.chaptertext_html = sanitizeInput(self.chaptertext)
        self.chaptersummary_html = sanitizeInput(self.chaptersummary)
        super(Chapter, self).save(*args, **kwargs)


class Comment(models.Model):
    parent = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dateposted = models.DateTimeField()
    commenttext = models.CharField(max_length=4250)
    commenttext_html = models.TextField(default='')
    isdeleted = models.BooleanField(default=False)

    def get_anchor_prefix(self):
        return 'c'

    def get_absolute_url(self):
        return f"{reverse('chapter-only-view', args=[self.parent.id])}#c{self.id}"

    def save(self, *args, **kwargs):
        self.commenttext_html = sanitizeMarkdown(self.commenttext)
        super().save(*args, **kwargs)
