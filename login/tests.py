from django_webtest import WebTest
from django.contrib.auth.models import User
from profiles.models import UserProfile


class TestRegistration(WebTest):
    @classmethod
    def try_signup(self, app):
        res = app.get('/login/signup')
        form = res.form
        form['screenname'] = 'Alexander Hamilton'
        form['loginname'] = 'hamilton'
        form['password1'] = 'raiseaGlass3'
        form['password2'] = 'raiseaGlass3'
        return form.submit()

    def test_loadpage(self):
        self.app.get('/login/signup')

    # Check that a user is actually made when signup
    def test_signup(self):
        self.try_signup(self.app)
        try:
            User.objects.get(username='hamilton')
        except User.DoesNotExist:
            self.fail('User was not created')

    def test_profile_created(self):
        self.try_signup(self.app)
        try:
            UserProfile.objects.get(screenname='Alexander Hamilton')
        except UserProfile.DoesNotExist:
            self.fail('UserProfile not created')

    # Check that user is redirected to front page after signup
    def test_redirect(self):
        res = self.try_signup(self.app)
        '''
        At the moment, only checks that it redirects at all.
        TODO: Test that the following page is, indeed, the front page.
        '''
        res = res.follow()
