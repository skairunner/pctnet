from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.shortcuts import reverse

from django_webtest import WebTest
from django_dynamic_fixture import G

from profiles.models import UserProfile
from .models import PrivateMessageGroup
from .views import UsernamesField


class TestUsernamesField(WebTest):
    def test_max_obeyed(self):
        users = []
        profiles = []
        for x in range(3):
            users.append(G(User))
        for user in users:
            profiles.append(G(UserProfile, user=user))
        field = UsernamesField(max_users=2)
        input = ','.join([profile.screenname for profile in profiles])
        try:
            field.clean(input)
            self.fail('Field unexpectedly validated with too many inputs')
        except ValidationError as e:
            if e.code != 'usercount':
                self.fail(f'Unexpected validation error {e.code}')

    def test_one_input(self):
        user = G(User)
        profile = G(UserProfile, user=user)
        field = UsernamesField()
        self.assertEquals(field.clean(profile.screenname)[0].pk, user.pk)

    def test_some_inputs(self):
        users = []
        profiles = []
        for x in range(3):
            users.append(G(User))
        for user in users:
            profiles.append(G(UserProfile, user=user))
        input = ','.join([profile.screenname for profile in profiles])
        field = UsernamesField()
        output = field.clean(input)
        for i in range(3):
            self.assertEquals(users[i].pk, output[i].pk)

    def test_invalid_user(self):
        user = G(User)
        G(UserProfile, user=user, screenname='foo')
        field = UsernamesField()
        try:
            field.clean('bar')
            self.fail('Validation unexpectedly succeeded on invalid username')
        except ValidationError as e:
            if e.code != 'username':
                self.fail(f'Unexpected error thrown: {e.code}')


class TestGroupPMs(WebTest):
    def make_default_users(self):
        u1 = G(User, username='u1')
        u2 = G(User, username='u2')
        u3 = G(User, username='u3')
        users = [u1, u2, u3]
        p1 = G(UserProfile, user=u1, screenname='user1')
        p2 = G(UserProfile, user=u2, screenname='user2')
        p3 = G(UserProfile, user=u3, screenname='user3')
        profiles = [p1, p2, p3]
        return users, profiles

    def test_make_dm(self):
        self.make_default_users()
        res = self.app.get(reverse('makegroupmsg'), user='u1')
        form = res.form
        form['participants'] = 'user2'
        form['title'] = 'title'
        form['firstmessage'] = 'Hello World'
        form.submit('submit').follow()
        try:
            dm = PrivateMessageGroup.objects.get(title='title')
        except PrivateMessageGroup.DoesNotExist:
            self.fail('DM was not created')
        # These two should succeed
        self.app.get(dm.get_absolute_url(), user='u1')
        self.app.get(dm.get_absolute_url(), user='u2')
        # This should not.
        res = self.app.get(dm.get_absolute_url(), user='u3', expect_errors=True)
        self.assertIn('403', res.status)
