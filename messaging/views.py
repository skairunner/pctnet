from django import forms
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, FormView

from dj_preview_mixin import PreviewMixin
from sanitize import sanitizeInput
from profiles.models import UserProfile
from rules.contrib.views import PermissionRequiredMixin

from .models import PrivateMessageGroup, PrivateMessage


# expects: Comma-separated list of usernames (exact)
# returns: List of User objects
class UsernamesField(forms.Field):
    max_users = None

    def __init__(self, *args, max_users=None, **kwargs):
        self.max_users = max_users
        super().__init__(*args, **kwargs)

    def clean(self, value):
        maybe_usernames = [x.strip() for x in value.split(',')]
        if self.max_users and len(maybe_usernames) \
                >= self.max_users:
            raise ValidationError('Too many users; max length is %(users)s',
                    code='usercount',
                    params={'users': self.max_users})

        users = []
        for maybe_username in maybe_usernames:
            try:
                profile = UserProfile.objects.get(screenname=maybe_username)
                users.append(profile.user)
            except ObjectDoesNotExist:
                raise ValidationError('User %(maybeuser)s does not exist', code='username', params={'maybeuser': maybe_username})
        return users


class MakePMForm(forms.Form):
    participants = UsernamesField(max_users=9)
    title = forms.CharField(max_length=255)
    firstmessage = forms.CharField(widget=forms.Textarea)


class MakePMView(LoginRequiredMixin, PreviewMixin, FormView):
    template_name = 'messaging/pm-make.html'
    form_class = MakePMForm

    def preprocess_preview(self, form, context):
        content = form.cleaned_data['firstmessage']
        context['preview_markup'] = sanitizeInput(content)
        context['preview_title'] = form.cleaned_data['title']

    # actually process it
    def form_valid_nopreview(self, form):
        group = PrivateMessageGroup(owner=self.request.user,
                title=form.cleaned_data['title'])
        group.save()
        users = form.cleaned_data['participants']
        group.members.add(*users)
        group.members.add(self.request.user)
        group.save()
        msg = PrivateMessage(parent=group)
        msg.author = self.request.user
        msg.content = form.cleaned_data['firstmessage']
        msg.save()

        return HttpResponseRedirect(group.get_absolute_url())


class PMView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = PrivateMessageGroup
    template_name = 'messaging/pm-view.html'
    permission_required = 'messaging.view_privatemessagegroup'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        msgs = self.object.privatemessage_set.order_by('timestamp').all()
        kwargs['messages'] = msgs
        return kwargs
