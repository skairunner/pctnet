from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms import DateInput
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from .models import UserProfile


class UserProfileView(DetailView):
    model = UserProfile


def UserRedirect(request, *args, **kwargs):
    obj = get_object_or_404(UserProfile, pk=kwargs["pk"])
    return HttpResponseRedirect(reverse("viewuser", args=[obj.pk, obj.slug]))


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    fields = ["slug", "bio"]
    model = UserProfile
    template_name = "profiles/profile_update.html"
    
    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        response = super(ProfileUpdateView, self).get(*args, **kwargs)
        if self.object.user.id == self.request.user.id:
            return response
        raise Http404("No permission to edit user bio.")
