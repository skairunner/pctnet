from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.text import slugify
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from datetime import datetime
from dj_commented_view import CommentPostMixin, CommentListMixin

from .models import Group, GroupComment


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
        obj.admins.add(self.request.user)
        obj.members.add(self.request.user)
        obj.save()
        return self.get_success_url()


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
