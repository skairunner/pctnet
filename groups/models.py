from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from stories.models import Story


class Group(models.Model):
    groupname = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(default='')
    members = models.ManyToManyField(User, related_name='memberof')
    founder = models.ForeignKey(User, related_name='founded', on_delete=models.CASCADE)
    admins = models.ManyToManyField(User, related_name='adminof')
    mods = models.ManyToManyField(User, related_name='modof')
    grouppage = models.TextField(default='')

    def get_absolute_url(self):
        return reverse('group-homepage', args=[self.id, self.slug])


class GroupFolders(models.Model):
    parent = models.ForeignKey(Group, on_delete=models.CASCADE)
    stories = models.ManyToManyField(Story, related_name='infolder')


class GroupComment(models.Model):
    parent = models.ForeignKey(Group, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dateposted = models.DateTimeField()
    commenttext = models.CharField(max_length=4250)
    isdeleted = models.BooleanField(default=False)


class GroupForum(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)  # possibly add support for a hidden mod forum, or other special forums


class GroupForumThread(models.Model):
    forum = models.ForeignKey(GroupForum, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    threadname = models.CharField(max_length=255)
    dateposted = models.DateTimeField()
    slug = models.SlugField(default='')

    def get_absolute_url(self):
        slug = f'{self.forum.group.slug}.{self.slug}'
        return reverse('viewthread', args=[
            self.forum.group.id,
            self.id,
            slug
        ])


class GroupForumThreadPost(models.Model):
    thread = models.ForeignKey(GroupForumThread, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    postcontent = models.TextField()
    dateposted = models.DateTimeField()

    def get_absolute_url(self):
        return f'{self.thread.get_absolute_url()}#post{self.id}'
