from django.contrib.auth.mixins import LoginRequiredMixin
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


class UserProfileView(DetailView):
    model = UserProfile


def UserRedirect(request, *args, **kwargs):
    obj = get_object_or_404(UserProfile, pk=kwargs["pk"])
    return HttpResponseRedirect(reverse("viewuser", args=[obj.pk, obj.slug]))


class ProfileUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    fields = ["slug", "bio"]
    model = UserProfile
    permission_required = 'profiles.change_profile'
    template_name = "profiles/profile_update.html"


def current_user(request):
    return HttpResponse("<html><body><p>%s</p></body></html>" % (request.user.pk,))
