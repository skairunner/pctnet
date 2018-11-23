from profiles.models import UserProfile
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.db import IntegrityError
from django.forms import ModelForm, Form
import django.forms as forms


class UserProfileForm(ModelForm):
    loginname = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=128)
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=128)

    class Meta:
        model = UserProfile
        fields = ['screenname']

    def clean(self):
        cleaned = super().clean()
        pw1 = cleaned.get('password1')
        pw2 = cleaned.get('password2')
        # pw1/pw2 might not exist
        if pw1 and pw2:
            if pw1 != pw2:
                raise forms.ValidationError('Your passwords do not match.')
        screenname = cleaned.get('screenname')
        try:
            userobj = User.objects.create_user(username=cleaned.get('loginname'), email='', password=cleaned.get('password1'))
        except IntegrityError:
            raise forms.ValidationError("Someone is using your chosen login name")
        try:
            UserProfile.objects.create(user=userobj, screenname=screenname, slug=slugify(screenname))
        except IntegrityError:
            userobj.delete()
            raise forms.ValidationError("Someone is using your chosen screenname")

        return cleaned


class SignupView(FormView):
    template_name = "login/registration.html"
    form_class = UserProfileForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):

        return super().form_valid(form)
