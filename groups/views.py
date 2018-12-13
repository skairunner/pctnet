from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.text import slugify
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from .models import Group


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


class GroupHomepageView(DetailView):
    model = Group
