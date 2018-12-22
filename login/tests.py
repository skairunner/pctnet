from django_webtest import WebTest
from django.contrib.auth.models import User
from profiles.models import UserProfile


class TestRegistration(WebTest):
    def try_signup(self, **kwargs):
        res = self.app.get('/login/signup')
        form = res.form
        form['screenname'] = 'Alexander Hamilton'
        form['loginname'] = 'hamilton'
        form['password1'] = 'raiseaGlass3'
        form['password2'] = 'raiseaGlass3'
        for key, val in kwargs.items():
            form[key] = val
        return form.submit()

    def test_loadpage(self):
        self.app.get('/login/signup')

    # Check that a user is actually made when signup
    def test_signup(self):
        self.try_signup()
        try:
            User.objects.get(username='hamilton')
        except User.DoesNotExist:
            self.fail('User was not created')

    def test_profile_created(self):
        self.try_signup()
        try:
            UserProfile.objects.get(screenname='Alexander Hamilton')
        except UserProfile.DoesNotExist:
            self.fail('UserProfile not created')

    # Check that user is redirected to front page after signup
    def test_redirect(self):
        res = self.try_signup()
        '''
        At the moment, only checks that it redirects at all.
        TODO: Test that the following page is, indeed, the front page.
        '''
        res = res.follow()

    def test_duplicated_loginname_errors(self):
        self.try_signup()
        res = self.try_signup(screenname='not_ham')
        self.assertIn('using this loginname', res.text)

    def test_duplicated_screenname_errors(self):
        self.try_signup()
        res = self.try_signup(loginname='not_ham')
        self.assertIn('using this screenname', res.text)

    def test_checks_passwords_filled(self):
        res = self.try_signup(password1='')
        self.assertIn('input your password twice', res.text)
        res = self.try_signup(password2='')
        self.assertIn('input your password twice', res.text)

    def test_checks_passwords_match(self):
        res = self.try_signup(password1='ajdk20d9s', password2='ask30ms1')
        self.assertIn('do not match', res.text)
