from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms import DateInput
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from rules.contrib.views import PermissionRequiredMixin

from .models import UserProfile


def redirectFullUserPath(userid):
    user = get_object_or_404(User, id=userid)
    return HttpResponseRedirect(user.userprofile.get_full_url())


@login_required
def CurrentUserRedirect(request):
    return redirectFullUserPath(request.user.id)


class UserProfileView(DetailView):
    model = UserProfile


def UserRedirect(request, *args, **kwargs):
    return redirectFullUserPath(kwargs['pk'])


class ProfileUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    fields = ["slug", "bio"]
    model = UserProfile
    permission_required = 'profiles.change_profile'
    template_name = "profiles/profile_update.html"
