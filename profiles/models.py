from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    screenname = models.CharField(max_length=50)
    slug = models.SlugField(default="")
    bio = models.TextField(default="")

    def get_absolute_url(self):
        return reverse("viewuser", args=[self.user.id, self.slug])
