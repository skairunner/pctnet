from django_webtest import WebTest
from django.contrib.auth.models import User
from profiles.models import UserProfile


class TestRegistration(WebTest):
    def try_signup(self, **kwargs):
        res = self.app.get('/signup/')
        form = res.form
        form['screenname'] = 'Alexander Hamilton'
        form['loginname'] = 'hamilton'
        form['password1'] = 'raiseaGlass3'
        form['password2'] = 'raiseaGlass3'
        for key, val in kwargs.items():
            form[key] = val
        return form.submit()

    def check_user_exists(self, loginname='hamilton'):
        try:
            User.objects.get(username=loginname)
            return True
        except User.DoesNotExist:
            return False

    def check_profile_exists(self, screenname='Alexander Hamilton'):
        try:
            UserProfile.objects.get(screenname=screenname)
            return True
        except UserProfile.DoesNotExist:
            return False

    def check_redirect(self, redirect_url, user_id='5', username='alexander-hamilton'):
        return redirect_url == f'/user/{user_id}/{username}/'

    def test_loadpage(self):
        self.app.get('/signup/')

    # Check that a user is actually made when signup
    def test_signup(self):
        self.try_signup()
        self.assertTrue(self.check_user_exists(), 'User was not created')
        self.assertTrue(self.check_profile_exists(), 'UserProfile was not created')

    # Check that user is redirected to front page after signup
    def test_redirect(self):
        res = self.try_signup()
        res = res.follow()
        self.assertTrue(self.check_redirect(res.url), 'User was not directed to home page on account creation')

    def test_duplicated_loginname_errors(self):
        self.try_signup()
        res = self.try_signup(screenname='not_ham')
        self.assertIn('using this loginname', res.text)
        self.assertFalse(self.check_profile_exists('not_ham'), 'User was erronously created')

    def test_duplicated_screenname_errors(self):
        self.try_signup()
        res = self.try_signup(loginname='not_ham')
        self.assertIn('using this screenname', res.text)
        self.assertFalse(self.check_user_exists('not_ham'), 'UserProfile was erronously created')

    def test_checks_passwords_filled(self):
        res = self.try_signup(password1='')
        self.assertIn('input your password twice', res.text)
        self.assertFalse(self.check_user_exists(), 'User was erronously created')
        res = self.try_signup(password2='')
        self.assertIn('input your password twice', res.text)
        self.assertFalse(self.check_user_exists(), 'User was erronously created')

    def test_checks_passwords_match(self):
        res = self.try_signup(password1='ajdk20d9s', password2='sk30ms1')
        self.assertIn('do not match', res.text)
        self.assertFalse(self.check_user_exists(), 'User was erronously created')
