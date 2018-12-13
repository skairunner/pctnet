from django.conf import settings
from django.db import models
from django.urls import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)
    screenname = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(default="")
    bio = models.TextField(default="")

    def get_full_url(self):
        return reverse('viewuser', args=[self.pk, self.slug])

    def get_absolute_url(self):
        return self.get_full_url()
