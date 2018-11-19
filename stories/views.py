from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import DateInput
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .models import Story, Chapter


class ChapterDetailView(DetailView):
    model = Chapter
    pk_url_kwarg = 'chapterpk'

    def get_context_data(self, **kwargs):
        data = super(ChapterDetailView, self).get_context_data(**kwargs)
        # Get chapter list and current chapter
        chapterset = self.object.parent.chapter_set.all().order_by('chapterorder')
        # Find current
        i = 0
        for chap in chapterset:
            if self.object.id == chap.id:
                break
            i += 1
        if i - 1 >= 0:
            data['previous_chapter'] = chapterset[i-1].get_absolute_url()
        if i + 1 < len(chapterset):
            data['next_chapter'] = chapterset[i+1].get_absolute_url()
        # List of all chapters
        data['chapter_list'] = [(i+1, x.id, x.chaptertitle) for i, x in enumerate(chapterset)]
        data['this_chapter'] = self.object.id
        return data



# Non-slugged chapter to slugged chapter
def ChapterRedirect(request, *args, **kwargs):
    obj = get_object_or_404(Chapter, pk=kwargs["chapterpk"])
    slug = f"{obj.parent.slug}.{obj.slug}"
    return HttpResponseRedirect(reverse("viewchapter", args=[obj.parent.pk, obj.pk, slug]))


# Redirects non-slugged story to slugged story
def StoryRedirect(request, *args, **kwargs):
    obj = get_object_or_404(Story, pk=kwargs["pk"])
    return HttpResponseRedirect(reverse("viewstory", args=[obj.pk, obj.slug]))


# It's a redirect now, but may want Ao3-esque archive warnings
# page in the future
def StoryToChapterRedirect(request, *args, **kwargs):
    obj = get_object_or_404(Story, pk=kwargs["pk"])
    ch = get_object_or_404(Chapter, pk=obj.firstchapter_id)
    slug = f"{obj.slug}.{ch.slug}"
    return HttpResponseRedirect(reverse("viewchapter", args=[obj.pk, obj.firstchapter_id, slug]))


class StorySubmitView(LoginRequiredMixin, CreateView):
    fields = ["chaptertitle", "dateposted", "chaptertext"]
    model = Chapter # easier to backfill Story from Chapter
    template_name = "stories/story_submit.html"

    def get_form(self, form_class=None):
        form = super(StorySubmitView, self).get_form(form_class)
        form.fields['dateposted'].widget = DateInput(attrs={"type": "date"})
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        # Also produce a parent object
        story = Story()
        story.owner = self.object.author
        story.datefirstposted = story.datelastposted = self.object.dateposted
        story.worksummary = self.object.chaptersummary
        # Empty field to prevent weirdness when convert to multichapter
        self.object.chaptersummary = ""
        story.worktitle = self.object.chaptertitle
        self.object.chaptertitle = "" # same
        # Commit to db
        story.save()
        self.object.parent = story
        self.object.save()
        # Set first chapter!
        story.firstchapter = self.object
        story.save()

        self.object = story # temporary while making new url
        return HttpResponseRedirect(self.get_success_url())
