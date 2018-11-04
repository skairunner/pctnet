from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import DateInput
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .models import Story


class StoryDetailView(DetailView):
    model = Story


def StoryRedirect(request, *args, **kwargs):
    obj = get_object_or_404(Story, pk=kwargs["pk"])
    return HttpResponseRedirect(reverse("viewstory", args=[obj.pk, obj.slug]))


class StorySubmitView(LoginRequiredMixin, CreateView):
    fields = ["worktitle", "dateposted", "worktext"]
    model = Story
    template_name = "stories/story_submit.html"

    def get_form(self, form_class=None):
        form = super(StorySubmitView, self).get_form(form_class)
        form.fields['dateposted'].widget = DateInput(attrs={"type": "date"})
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
