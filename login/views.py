from profiles.models import UserProfile
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.db import IntegrityError, transaction
from django.forms import Form
import django.forms as forms


class UserProfileForm(Form):
    loginname = forms.CharField(max_length=150)
    screenname = forms.CharField(max_length=50)
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=128)
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=128)

    def clean(self):
        cleaned = super().clean()
        pw1 = cleaned.get('password1')
        pw2 = cleaned.get('password2')
        # pw1/pw2 might not exist
        if pw1 and pw2:
            if pw1 != pw2:
                raise forms.ValidationError('Your passwords do not match.')
        else:
            raise forms.ValidationError('You forgot to input your password twice.')
        return cleaned


class SignupView(FormView):
    template_name = "login/registration.html"
    form_class = UserProfileForm
    success_url = reverse_lazy('login')

    def report_error(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        screenname = form.cleaned_data['screenname']
        loginname = form.cleaned_data['loginname']
        pwd = form.cleaned_data['password1']

        try:
            with transaction.atomic():
                userobj = User.objects.create_user(
                    username=loginname,
                    email='',
                    password=pwd
                )
                UserProfile.objects.create(
                    user=userobj,
                    screenname=screenname,
                    slug=slugify(screenname)
                )
        except IntegrityError as e:
            if 'username' in repr(e.__cause__):
                form.add_error('loginname', 'Someone is already using this loginname.')
            elif 'screenname' in repr(e.__cause__):
                form.add_error('screenname', 'Someone is already using this screenname.')
            return self.report_error(form)

        return HttpResponseRedirect(self.get_success_url())
