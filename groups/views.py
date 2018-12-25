from django import forms
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.urls import reverse
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from datetime import datetime
from dj_commented_view import CommentPostMixin, CommentListMixin
import rules

from .models import Group, GroupComment, GroupForum, GroupForumThread, GroupForumThreadPost


class GroupIndex(ListView):
    model = Group
    template_name = 'groups/group-list.html'


def redirectGroup(request, pk):
    group = Group.objects.get(id=pk)
    return HttpResponseRedirect(reverse('group-homepage', args=[pk, group.slug]))


class CreateGroupView(LoginRequiredMixin, CreateView):
    model = Group
    fields = ['groupname', 'grouppage']
    template_name = 'groups/group_create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.founder = self.request.user
        obj.slug = slugify(obj.groupname)
        obj.save()
        self.object = obj
        # Create forum
        forum = GroupForum(group=obj)
        forum.save()
        # Finish setting up group
        obj.admins.add(self.request.user)
        obj.members.add(self.request.user)
        obj.save()
        return HttpResponseRedirect(self.get_success_url())


class GroupHomepageEdit(LoginRequiredMixin, UpdateView):
    model = Group
    fields = ['grouppage']
    template_name = 'groups/group-edit.html'

    # Bounce if not allowed
    def dispatch(self, request, *args, **kwargs):
        if not rules.test_rule('can_edit_grouppage', request.user, self.get_object()):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class GroupHomepageView(CommentPostMixin, CommentListMixin, DetailView):
    model = Group
    commentmodel = GroupComment
    parentfield = 'parent'
    postcomment_fields = ['commenttext']

    def get_comment_queryset(self):
        queryset = super().get_comment_queryset()
        return queryset.filter(isdeleted=False)

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        return super().post(*args, **kwargs)

    def postcomment_form_valid(self, form):
        comment = form.save(commit=False)
        setattr(comment, self.parentfield, self.object)
        comment.dateposted = datetime.now()
        comment.author = self.request.user
        comment.save()
        return HttpResponseRedirect(self.get_postcomment_success_url())


def redirectForum(request, grouppk):
    group = get_object_or_404(Group, id=grouppk)
    url = reverse('forum', args=[grouppk, group.slug])
    return HttpResponseRedirect(url)


class GroupForumView(ListView):
    model = GroupForumThread
    template_name = 'groups/forum.html'
    group = None

    def get_queryset(self):
        group = self.get_group()
        forum = group.groupforum_set.all()[0]
        qs = GroupForumThread.objects.filter(forum=forum).all()
        return qs

    def get_group(self):
        if self.group:
            return self.group
        self.group = Group.objects.get(id=self.kwargs['grouppk'])
        return self.group

    def get_context_data(self, **kwargs):
        kwargs['group'] = self.get_group()
        return super().get_context_data(**kwargs)


def redirectNewThread(request, grouppk):
    group = Group.objects.get(id=grouppk)
    url = reverse('newthread', args=[group.id, group.slug])
    return HttpResponseRedirect(url)


class NewThreadForm(forms.Form):
    threadname = forms.CharField(max_length=255)
    postcontent = forms.CharField()


class GroupThreadCreate(LoginRequiredMixin, FormView):
    template_name = 'groups/thread-create.html'
    form_class = NewThreadForm

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_forum(self):
        group = Group.objects.get(id=self.kwargs['grouppk'])
        return group.groupforum_set.all()[0]

    def form_valid(self, form):
        threadname = form.cleaned_data['threadname']
        now = datetime.now()
        thread = GroupForumThread(
            forum=self.get_forum(),
            author=self.request.user,
            dateposted=now,
            threadname=threadname,
            slug=slugify(threadname))
        thread.save()
        self.object = thread
        post = GroupForumThreadPost(
            thread=thread,
            author=self.request.user,
            postcontent=form.cleaned_data['postcontent'],
            dateposted=now)
        post.save()
        return HttpResponseRedirect(self.get_success_url())


def redirectViewThread(request, *args, **kwargs):
    thread = GroupForumThread.objects.get(id=kwargs['threadpk'])
    return HttpResponseRedirect(thread.get_absolute_url())


class ThreadView(CommentPostMixin, ListView):
    model = GroupForumThreadPost
    template_name = 'groups/thread-view.html'
    thread = None
    commentmodel = GroupForumThreadPost
    postcomment_fields = ['postcontent']
    parentfield = 'thread'

    def get_object(self):
        return GroupForumThreadPost()

    def get_thread(self):
        if not self.thread:
            self.thread = GroupForumThread.objects.get(id=self.kwargs['threadpk'])
        return self.thread

    def get_queryset(self):
        thread = self.get_thread()
        return GroupForumThreadPost \
            .objects \
            .filter(thread=thread.id) \
            .order_by('dateposted') \
            .all()

    def get_context_data(self, **kwargs):
        kwargs['thread'] = self.get_thread()
        kwargs['group'] = self.get_thread().forum.group
        return super().get_context_data(**kwargs)

    def postcomment_form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.dateposted = datetime.now()
        post.thread = self.get_thread()
        post.save()
        return HttpResponseRedirect(post.get_absolute_url())


def redirectPost(request, *args, **kwargs):
    post = GroupForumThreadPost.objects.get(id=kwargs['pk'])
    return HttpResponseRedirect(post.get_absolute_url())


class EditPostView(UpdateView):
    model = GroupForumThreadPost
    template_name = 'groups/post-edit.html'
    fields = ['postcontent']
