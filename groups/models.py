from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    groupname = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(default='')
    members = models.ManyToManyField(User, related_name='memberof')
    founder = models.ForeignKey(User, related_name='founded', on_delete=models.CASCADE)
    admins = models.ManyToManyField(User, related_name='adminof')
    mods = models.ManyToManyField(User, related_name='modof')
    group_page = models.TextField(default='')


class GroupComment(models.Model):
    parent = models.ForeignKey(Group, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dateposted = models.DateTimeField()
    commenttext = models.CharField(max_length=4250)


class GroupForum(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)  # possibly add support for a hidden mod forum, or other special forums


class GroupForumThread(models.Model):
    forum = models.ForeignKey(GroupForum, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    threadname = models.CharField(max_length=255)
    dateposted = models.DateTimeField()
    slug = models.SlugField(default='')

class GroupForumThreadPost(models.Model):
    thread = models.ForeignKey(GroupForumThread, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    postcontent = models.TextField()
    dateposted = models.DateTimeField()
