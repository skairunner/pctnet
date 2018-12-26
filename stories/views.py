from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import DateInput
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from dj_commented_view import CommentPostMixin, CommentListMixin
import rules
from rules.contrib.views import PermissionRequiredMixin

from datetime import datetime

from .models import Story, Chapter, Comment


def can_view_chapter(user, chapter):
    if chapter.isdraft or chapter.parent.isdraft:
        return rules.test_rule('can_view_chapter_draft', user, chapter)
    return True


def can_view_story(user, story):
    if story.isdraft:
        return rules.test_rule('can_view_story_draft', user, story)
    return True


class StoryIndexView(ListView):
    model = Story
    template_name = 'stories/story-index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(isdraft=False)


class ChapterDetailView(CommentPostMixin, CommentListMixin, DetailView):
    model = Chapter
    commentmodel = Comment
    parentfield = 'parent'
    pk_url_kwarg = 'chapterpk'
    postcomment_fields = ['commenttext']

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not can_view_chapter(self.request.user, obj):
           raise Http404()
        return obj

    def get_comment_queryset(self):
        queryset = super().get_comment_queryset()
        queryset = queryset.order_by('dateposted')
        return queryset.filter(isdeleted=False)

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        return super().post(*args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # Get chapter list and current chapter
        chapterset = [ch for ch in self.object.parent.chapter_set.all() if can_view_chapter(self.request.user, ch)]

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

        # Provide comments
        data['comments'] = self.object.comment_set.all().filter(isdeleted=False)

        return data

    def postcomment_form_valid(self, form):
        comment = form.save(commit=False)
        setattr(comment, self.parentfield, self.object)
        comment.dateposted = datetime.now()
        comment.author = self.request.user
        comment.save()
        return HttpResponseRedirect(self.get_postcomment_success_url())

# Non-slugged chapter to slugged chapter
def ChapterRedirect(request, *args, **kwargs):
    obj = get_object_or_404(Chapter, pk=kwargs["chapterpk"])
    if not can_view_chapter(request.user, obj):
        raise Http404()
    return HttpResponseRedirect(obj.get_absolute_url())


# Redirects non-slugged story to slugged story
def StoryRedirect(request, *args, **kwargs):
    obj = get_object_or_404(Story, pk=kwargs["pk"])
    if not can_view_story(request.user, obj):
        raise Http404()
    return HttpResponseRedirect(reverse("viewstory", args=[obj.pk, obj.slug]))


# It's a redirect now, but may want Ao3-esque archive warnings
# page in the future
def StoryToChapterRedirect(request, *args, **kwargs):
    obj = get_object_or_404(Story, pk=kwargs["pk"])
    if not can_view_story(request.user, obj):
        raise Http404()
    ch = get_object_or_404(Chapter, pk=obj.firstchapter_id)
    if not can_view_chapter(request.user, ch):
        raise Http404()
    slug = f"{obj.slug}.{ch.slug}"
    return HttpResponseRedirect(reverse("viewchapter", args=[obj.pk, obj.firstchapter_id, slug]))


class StorySubmitView(LoginRequiredMixin, CreateView):
    fields = ["chaptertitle", "dateposted", "chaptertext", "isdraft"]
    model = Chapter  # easier to backfill Story from Chapter
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
        self.object.chaptertitle = ""  # same
        # Commit to db
        story.save()
        self.object.parent = story
        self.object.save()
        # Set first chapter!
        story.firstchapter_id = self.object.id
        story.save()

        self.object = story # temporary while making new url
        return HttpResponseRedirect(self.get_success_url())


class ChapterSubmitView(CreateView):
    model = Chapter
    fields = ['dateposted', 'chaptertitle', 'chaptersummary', 'chaptertext', 'isdraft']
    template_name = 'stories/chapter_new.html'
    story = None

    def get_form(self, form_class=None):
        form = super(ChapterSubmitView, self).get_form(form_class)
        form.fields['dateposted'].widget = DateInput(attrs={"type": "date"})
        return form

    def get_story(self):
        if not self.story:
            self.story = Story.objects.get(id=self.kwargs['pk'])
        return self.story

    def get_context_data(self, **kwargs):
        s = self.get_story()
        buttons = getEditNavButtons(s, s.chapter_set.order_by('chapterorder').all(), -2)
        kwargs['buttons'] = buttons
        kwargs['story'] = s
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        chapter = form.save(commit=False)
        story = self.get_story()
        chapter.author = self.request.user
        chapter.parent = story
        chapter.chapterorder = story.chapter_set.order_by('-chapterorder').first().chapterorder + 1
        chapter.save()
        self.object = chapter
        return HttpResponseRedirect(self.get_success_url())


# Mark current chapter as True. Otherwise, mark Story as true
def getEditNavButtons(story, chapters, current=-1):
    buttons = [(c.chapterorder + 1, reverse('editchapter', args=[c.id]), True if current == c.chapterorder else False) for c in chapters]
    buttons.insert(0, ('Story', reverse('editstory', args=[story.id]), True if current == -1 else False))
    return buttons


class StoryEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Story
    fields = ['worktitle', 'worksummary', 'isdraft']
    template_name = 'stories/story_edit.html'
    permission_required = 'stories.change_story'

    def get_context_data(self, **kwargs):
        chapters = self.get_object().chapter_set.all().order_by('chapterorder').all()
        kwargs['buttons'] = getEditNavButtons(self.object, chapters)
        return super().get_context_data(**kwargs)


class ChapterEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Chapter
    fields = ['chaptertitle', 'chaptersummary', 'chaptertext', 'dateposted', 'isdraft']
    pk_url_kwarg = 'chapterpk'
    template_name = 'stories/chapter_edit.html'
    permission_required = 'stories.change_chapter'

    def get_form(self, form_class=None):
        form = super(ChapterEditView, self).get_form(form_class)
        form.fields['dateposted'].widget = DateInput(attrs={"type": "date"})
        return form

    def get_context_data(self, **kwargs):
        kwargs['story'] = self.object.parent
        kwargs['chapters'] = self.object.parent.chapter_set.all().order_by('chapterorder').all()
        kwargs['buttons'] = getEditNavButtons(self.object.parent, kwargs['chapters'], self.object.chapterorder)
        return super().get_context_data(**kwargs)


class CommentDeleteView(DeleteView):
    model = Comment

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.object.parent.get_absolute_url()
        self.object.isdeleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class CommentEditView(UpdateView):
    model = Comment
    fields = ['commenttext']
