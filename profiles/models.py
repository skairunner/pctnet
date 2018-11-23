from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)
    screenname = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(default="")
    bio = models.TextField(default="")

    def get_absolute_url(self):
        return reverse("viewuser", args=[self.user.id, self.slug])
